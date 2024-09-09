#ifndef INPUT_H
#define INPUT_H

#include "config.h"
#include "tcpserver.h"
#include <QCoreApplication>
#include <QSet>
#include <QVector>
#include <QPoint>
#include <QJsonDocument>
#include <QJsonObject>
#include <QEventLoop>
#include <QApplication>
#include <QDesktopWidget>
#include <QMap>
#include <QMutex>
#include <QMutexLocker>
#include <QMimeData>
#include <QtConcurrent>
#include <QList>
#include <KWayland/Client/registry.h>
#include <KWayland/Client/connection_thread.h>
#include <KWayland/Client/ddeseat.h>
#include <KWayland/Client/fakeinput.h>
#include <KWayland/Client/datacontrolsource.h>
#include <KWayland/Client/datacontroldevice.h>
#include <KWayland/Client/datacontroldevicemanager.h>
#include <KWayland/Client/datacontroloffer.h>
#include <iostream>
#include <cmath>
#include <fcntl.h>
#include <unistd.h>
#include <signal.h>
#include <linux/uinput.h>


class Input : public QObject
{
    Q_OBJECT
public:
    explicit Input(QObject *parent = nullptr);
    ~Input();

public slots:
    InputEvent processEvent(QByteArray jsonstr);
    void moveTo(int x, int y);
    void keyEvent(int code, int val);
    void scroll(InputEvent input);
    QByteArray createJsonString(int x, int y, QString text = "");
    QPoint getGlobalPosition();
    QPoint getGlobalScreenSize();
    void onMessage(QByteArray jsonstr, QTcpSocket *clientSocket);
    void setText(QString text);
    QString getText();
    void onDataControlDeviceV1(KWayland::Client::DataControlOfferV1* offer);
    void writeByte(const QString &mimeType, qint32 fd);
signals:

private:
    Config m_config;
    TcpServer m_server;
    KWayland::Client::Registry * m_registry = Q_NULLPTR;
    KWayland::Client::Seat *m_seat = Q_NULLPTR;
    KWayland::Client::FakeInput *m_fakeInput = Q_NULLPTR;
    KWayland::Client::DDESeat *m_ddeSeat = Q_NULLPTR;
    KWayland::Client::DDEPointer *m_ddePointer = Q_NULLPTR;
    KWayland::Client::DataControlDeviceV1 *m_dataControlDeviceV1=Q_NULLPTR;
    KWayland::Client::DataControlSourceV1 *m_dataControlSourceV1=Q_NULLPTR;
    KWayland::Client::DataControlDeviceManager *m_dataControlDeviceManager = Q_NULLPTR;
    QMimeData *m_mimeDataRead=Q_NULLPTR;
    QMap<KWayland::Client::DataControlSourceV1 *, QMimeData *> m_sendDataMap;
    QList<double> m_mouseEventList = {BTN_LEFT, BTN_RIGHT, BTN_MIDDLE};
};

#endif // INPUT_H
