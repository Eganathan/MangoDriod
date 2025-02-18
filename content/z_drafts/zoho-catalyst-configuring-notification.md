---
date: '2025-02-18T08:16:02+05:30' 
draft: true
title: 'Zoho Catalyst Configuring Notification'
---

Sometimes the actual documentation does not work as expected and hence we have to brute force and find solutions, this is one such journey with ZCatalyst so far:


https://docs.catalyst.zoho.com/en/cloud-scale/help/push-notifications/android/

Add these scopes to existing properties file:

```yml
oauthScopes: ...,ZohoCatalyst.notifications.mobile,ZohoCatalyst.notifications.mobile.register
//... => Existing Scopes

notificationAppID = 77699000000260009 \\ Your App Id
```

also ensure you have the following properties in your properties file otherwise it crashes

```yml
zcqlParser=V1
serverTLD=COM
StratusDomainSuffix=COM
```

clean and rebuild your project

now lets write a api service to handle the notification service:


```kotlin

@AndroidEntryPoint
class JotNotificationService : FirebaseMessagingService() {

    override fun onNewToken(token: String) {
        Log.d("FCM", "New token fetched: ${token}")
        this.application.setPannaiNotificationDeviceId(token)
        ZAuthSDK.registerNotification(token) // you can use the CatalystSDK here to register the notification
        Log.d("FCM", "New token updated on shared preference")
    }

    override fun onMessageReceived(message: RemoteMessage) {
        super.onMessageReceived(message)
        Log.d("FCM", "Message received: ${message.notification}")
        Log.d("FCM", "1: ${message}")

        message.data.forEach { Log.d("FCM", "key: ${it.key} value:${it.value}") }

        val title = message.data["msg"]
        val additionalInfoString = message.data["addInfo"]

        showNotification(title, additionalInfoString)
    }

    private fun showNotification(title: String?, body: String?) {
        val notificationManager =
            getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        val notificationId = System.currentTimeMillis().toInt()
        val channelId = "default_channel"

        // Create the notification channel (for Android O and above)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channelName = "Default Channel" // User-visible name
            val importance = NotificationManager.IMPORTANCE_DEFAULT
            val channel = NotificationChannel(channelId, channelName, importance)
            notificationManager.createNotificationChannel(channel)
        }

        // Set up the intent to open the MainActivity when the notification is clicked
        val intent = Intent(this, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(this, 0, intent, PendingIntent.FLAG_IMMUTABLE)

        // Build the notification
        val notification = NotificationCompat.Builder(this, channelId)
            .setContentTitle(title)
            .setContentText(body)
            .setSmallIcon(R.drawable.ic_app_icon)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .build()

        notificationManager.notify(notificationId, notification)
    }
}


//Just to store the token for testing now
object JotPreference {

    object JotNotifications {
        const val name: String = "jot_Push_Notifications"
        const val DeviceTokenKey: String = "jot_device_token"
    }

}

fun Context.getPannaiNotificationDeviceId(): String? {
    val preferenceKey = JotPreference.JotNotifications
    val deviceTokenId = getSharedPreferences(preferenceKey.name, Context.MODE_PRIVATE).getString(preferenceKey.DeviceTokenKey, null)
    return deviceTokenId
}

private fun Context.setPannaiNotificationDeviceId(deviceId: String) {
    val preferenceKey = JotPreference.JotNotifications
    Log.d("FCM", "Storing DeviceToken in pref")
    getSharedPreferences(preferenceKey.name, Context.MODE_PRIVATE).edit()
        .putString(preferenceKey.DeviceTokenKey, deviceId).apply()
    Log.d("FCM", "DeviceToken stored in pref Successfully: ${this.getPannaiNotificationDeviceId()}")
}
```

now handle user permission for notification and then you can now test it via the catalyst console: