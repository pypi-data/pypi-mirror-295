#include "input.h"
#include <QProcess>

Input::Input(QObject *parent)
    : QObject{parent}
{
    connect(&m_server, &TcpServer::message, this, &Input::onMessage);
    m_registry = new KWayland::Client::Registry(this);
    m_registry->create(KWayland::Client::ConnectionThread::fromApplication(this));
    m_registry->setup();
    connect(m_registry, &KWayland::Client::Registry::fakeInputAnnounced, this, [this] (quint32 name, quint32 version) {
       m_fakeInput = m_registry->createFakeInput(name, version, this);
       m_fakeInput->authenticate("wayland_autotool","NanJing AutoTestTool");
    });
    connect(m_registry, &KWayland::Client::Registry::seatAnnounced, this, [this] (quint32 name, quint32 version) {
       m_seat = m_registry->createSeat(name, version, this);
    });
    connect(m_registry, &KWayland::Client::Registry::ddeSeatAnnounced, this, [this] (quint32 name, quint32 version) {
       m_ddeSeat = m_registry->createDDESeat(name, version, this);
       m_ddePointer = m_ddeSeat->createDDePointer(this);
    });
    connect(m_registry, &KWayland::Client::Registry::dataControlDeviceManagerAnnounced, this, [this] (quint32 name, quint32 version) {
       m_dataControlDeviceManager = m_registry->createDataControlDeviceManager(name, version, this);
       if (m_dataControlDeviceManager != Q_NULLPTR)
       {
           m_dataControlDeviceV1=m_dataControlDeviceManager->getDataDevice(m_seat, this);
           if (!m_dataControlDeviceV1)
               return;
           connect(m_dataControlDeviceV1, &KWayland::Client::DataControlDeviceV1::dataOffered,
                   this, &Input::onDataControlDeviceV1);
       }
    });
    QTimer::singleShot(2000, this, [&]() {
        QPoint point(0,0);
        m_fakeInput->requestPointerMoveAbsolute(point);
        m_fakeInput->requestPointerButtonClick(Qt::MouseButton::LeftButton);
    });
}

Input::~Input()
{
}

void Input::setText(QString text)
{
    m_dataControlSourceV1 = m_dataControlDeviceManager->createDataSource(this);
    connect(m_dataControlSourceV1, &KWayland::Client::DataControlSourceV1::sendDataRequested, this, &Input::writeByte);
    QMimeData* m_mimeData = new QMimeData();
    m_mimeData->setText(text);
    m_sendDataMap.insert(m_dataControlSourceV1, m_mimeData);
    for (const QString &format : m_mimeData->formats()) {
        m_dataControlSourceV1->offer(format);
    }
    m_dataControlDeviceV1->setSelection(0, m_dataControlSourceV1);
}

QString Input::getText()
{
    return m_mimeDataRead->text();
}

void Input::writeByte(const QString &mimeType, qint32 fd)
{
    KWayland::Client::DataControlSourceV1 *dataSource = qobject_cast<KWayland::Client::DataControlSourceV1*>(sender());
    QFile f;
    if (f.open(fd, QFile::WriteOnly, QFile::AutoCloseHandle)) {
        QByteArray content = m_sendDataMap[dataSource]->text().toUtf8();
        const QByteArray &ba = content;
        f.write(ba);
        f.close();
        disconnect(dataSource);
        dataSource->destroy();
        delete (m_sendDataMap[dataSource]);
        delete dataSource;
        m_sendDataMap.remove(dataSource);
    }
}
void Input::onDataControlDeviceV1(KWayland::Client::DataControlOfferV1* offer)
{
    qDebug() << "data offered";
    if (!offer)
        return;

    if(m_mimeDataRead==nullptr)
    {
        m_mimeDataRead=new QMimeData();
    }else {
        delete m_mimeDataRead;
        m_mimeDataRead=new QMimeData();
    }
    m_mimeDataRead->clear();

    QList<QString> mimeTypeList = offer->offeredMimeTypes();
    int mimeTypeCount = mimeTypeList.count();

    // 将所有的数据插入到mime data中
    static QMutex setMimeDataMutex;
    static int mimeTypeIndex = 0;
    mimeTypeIndex = 0;
    for (const QString &mimeType : mimeTypeList) {
        int pipeFds[2];
        if (pipe(pipeFds) != 0) {
            qWarning() << "Create pipe failed.";
            return;
        }
        fcntl(pipeFds[0], F_SETFD, FD_CLOEXEC);
        fcntl(pipeFds[0], F_SETFL, O_SYNC);
        fcntl(pipeFds[1], F_SETFD, FD_CLOEXEC);
        fcntl(pipeFds[1], F_SETFL, O_SYNC);
        // 根据mime类取数据，写入pipe中
        offer->receive(mimeType, pipeFds[1]);
        close(pipeFds[1]);
        // 异步从pipe中读取数据写入mime data中
        QtConcurrent::run([pipeFds, this, mimeType, mimeTypeCount] {
            QFile readPipe;
            if (readPipe.open(pipeFds[0], QIODevice::ReadOnly)) {
                if (readPipe.isReadable()) {
                    const QByteArray &data = readPipe.readAll();
                    if (!data.isEmpty()) {
                        // 需要加锁进行同步，否则可能会崩溃
                        QMutexLocker locker(&setMimeDataMutex);
                        m_mimeDataRead->setData(mimeType, data);
                    } else {
                        qWarning() << "Pipe data is empty, mime type: " << mimeType;
                    }
                } else {
                    qWarning() << "Pipe is not readable";
                }
            } else {
                qWarning() << "Open pipe failed!";
            }
            close(pipeFds[0]);
            if (++mimeTypeIndex >= mimeTypeCount) {
                mimeTypeIndex = 0;
            }
        });
    }
}

void Input::onMessage(QByteArray jsonstr, QTcpSocket *clientSocket)
{
    InputEvent inputEvent = processEvent(jsonstr);
    switch (inputEvent.eventType) {
        case EV_KEY:
            keyEvent(inputEvent.event, inputEvent.x);
            break;
        case EV_REL:
            if (inputEvent.event == REL_WHEEL || inputEvent.event == REL_HWHEEL)
            {
                scroll(inputEvent);
            }
            break;
        case EV_ABS:
            moveTo(inputEvent.x, inputEvent.y);
            clientSocket->write(createJsonString(0, 0));
            clientSocket->flush();
            break;
        case (EV_MAX+1):
            {
                // 向客户端发送应答
                QPoint point = getGlobalPosition();
                clientSocket->write(createJsonString(point.x(), point.y()));
                clientSocket->flush();
            }
            break;
        case (EV_MAX+2):
            {
                // 向客户端发送应答
                QPoint point = getGlobalScreenSize();
                clientSocket->write(createJsonString(point.x(), point.y()));
                clientSocket->flush();
            }
            break;
        case (EV_MAX+3):
            {
                this->setText(inputEvent.text);
            }
            break;
        case (EV_MAX+4):
            {
                // 向客户端发送应答
                clientSocket->write(createJsonString(0, 0, getText()));
                clientSocket->flush();
            }
            break;
        default:
            printf("Unknown event\n");
            break;
    }
}


QPoint Input::getGlobalPosition()
{
    return m_ddePointer->getGlobalPointerPos().toPoint();
}

QPoint Input::getGlobalScreenSize()
{
    int width=QApplication::desktop()->width();
    int height=QApplication::desktop()->height();
    QPoint size(width,height);
    return size;
}

InputEvent Input::processEvent(QByteArray jsonstr) {

    // 将JSON数据转换为InputEvent结构体
    InputEvent inputEvent;
    // 解析 JSON 数据
    QJsonDocument jsonDoc = QJsonDocument::fromJson(jsonstr);
    if (jsonDoc.isNull() || !jsonDoc.isObject()) {
        qWarning() << "JSON 解析失败或不是一个 JSON 对象";
        exit(-1);
    }

    QJsonObject jsonObj = jsonDoc.object();

    // 提取数据
    if (jsonObj.contains("eventType") && jsonObj["eventType"].isDouble()) {
        inputEvent.eventType = jsonObj["eventType"].toInt();
    }

    if (jsonObj.contains("x") && jsonObj["x"].isDouble()) {
        inputEvent.x = jsonObj["x"].toInt();
    }

    if (jsonObj.contains("y") && jsonObj["y"].isDouble()) {
        inputEvent.y = jsonObj["y"].toInt();
    }

    if (jsonObj.contains("event") && jsonObj["event"].isDouble()) {
        inputEvent.event = jsonObj["event"].toInt();
    }

    if (jsonObj.contains("text") && jsonObj["text"].isString()) {
        inputEvent.text = jsonObj["text"].toString();
    }

    // 打印结构体内容作为示例
    printf("Event: %d X: %d Y: %d\n", inputEvent.event, inputEvent.x, inputEvent.y);

    return inputEvent;
}

void Input::moveTo(int x, int y)
{
    QPoint point(x,y);
    m_fakeInput->requestPointerMoveAbsolute(point);
}

void Input::keyEvent(int code, int val)
{
    if (m_mouseEventList.contains(code))
    {
        if(val == 0x1)
        {
            m_fakeInput->requestPointerButtonPress(code);
        }else if (val == 0x0)
        {
            m_fakeInput->requestPointerButtonRelease(code);
        }
    }else
    {
        if(val == 0x1)
        {
            m_fakeInput->requestKeyboardKeyPress(code);
        }else if (val == 0x0)
        {
            m_fakeInput->requestKeyboardKeyRelease(code);
        }
    }
}

void Input::scroll(InputEvent input)
{
    if(input.event == 0x06)
    {
        m_fakeInput->requestPointerAxis(Qt::Orientation::Horizontal,input.x);
    }
    else if(input.event == 0x08)
    {
        m_fakeInput->requestPointerAxis(Qt::Orientation::Vertical,input.x);
    }

}

QByteArray Input::createJsonString(int x, int y, QString text) {
    // 创建一个 JSON 对象
    QJsonObject jsonObj;
    jsonObj["x"] = x;
    jsonObj["y"] = y;
    jsonObj["text"] = text;

    // 将 JSON 对象转换为 JSON 文档
    QJsonDocument jsonDoc(jsonObj);

    // 将 JSON 文档转换为 JSON 字符串
    QString jsonString = jsonDoc.toJson(QJsonDocument::Compact);

    // 返回 JSON 字符串
    return jsonString.toUtf8();
}
