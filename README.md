# Blynk SmartThings Integration 

### (Previously Blynk Smartthings Bridge)

A Smartthings SmartApp that bridges your Blynk devices into the SmartThings ecosystem using virtual switches. 

This integration allows you to control your Blynk devices directly from the SmartThings app or One UI native integrations, enabling integration with SmartThings scenes, automations, and voice assistants Google Home without requiring the Blynk.

## Why this exists?

I found myself managing a large number of Blynk.io devices, but I grew tired of switching back and forth between apps just to control my devices. I wanted a unified experience where all my home automation devices lived in one place. 
By building this bridge, I’ve effectively "exported" my Blynk controls into SmartThings, allowing me to treat my Blynk devices as native SmartThings devices, control them via routines and use all available integrations via Smartthings.

As an added bonus if you have a samsung phone, the controls gets integrated natively into the device control panel.

---

## Features

* **Unified Control:** Manage Blynk resources via the native SmartThings interface.
* **Dynamic Mapping:** Easily pair any number of SmartThings virtual switches to specific Blynk Devices.
* **Status Syncing:** Automatically triggers events in Blynk when you toggle a switch in SmartThings.
* **Deployment Ready:** Deploy directly on render or google cloud on free tier.

---

## How it Works

This application acts as a secure middleware webhook:

1. The app registers with SmartThings and listens for configuration and event updates.
2. During installation, you map a specific SmartThings switch to a Blynk Virtual Pin.
3. When you toggle a switch in SmartThings, it sends a `DEVICE_EVENT` to this app.
4. The app identifies which Blynk resource is associated with that device ID and sends the corresponding command to the Blynk API.

---

## How to Install

Follow these steps to deploy and register your bridge application.

### 1. Deploy the Application

Deploy the application to your preferred hosting service (e.g., Render, GCP App Engine, or any VPS).

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Ryuga/Blynk-Smartthings-Integration)

* **Environment Variables:**
* You can configure `NUMBER_OF_DEVICES` (default is 5).
* `TARGET_URL` Provide the domain where SmartThings will send requests. If you are using Render, you can use the auto-generated domain (e.g., `https://your-app.onrender.com`leave the field empty and, it will automatically set this value). If you have a custom domain attached, you may use that instead.

### 2. Register in SmartThings Workspace

1. Log in to the [SmartThings Developer Workspace](https://developer.smartthings.com/workspace).
2. Create a new project of type **"Automation for the SmartThings App"**.
3. Provide a name, then click **Register App**.
4. Select **Webhook Endpoint** as the hosting type.
5. When prompted for the Target URL, provide your domain appended with `/smartapp` (e.g., `https://your-domain.com/smartapp`).
* *Note: The `/smartapp` path is required for the Developer Console registration, even though your actual application will handle the endpoint internally.*


6. Enter a name and description, then select the following **Permissions**:
* `i:deviceprofiles:*`
* `r:devices:*`
* `w:devices:*`
* `x:devices:*`


7. Click **Next** and **Save**.
8. **Important:** Copy your **Client ID** and **Client Secret** and store them in a secure place. While not currently used by this version of the app, they may be required for future management features.

### 3. Verify and Deploy

1. **Verify Registration:** With your service running on your hosting provider, click the verification button in the workspace. SmartThings will ping your service to confirm the webhook is live.
2. **Deploy to Test:** Move to the **Test** tab in the developer console. Ensure **Developer Mode** is toggled on, then click **Deploy to Test**.

### 4. Setup in SmartThings App

> Create **Virtual Switches** first via the "SmartThings Labs" option in the app if you haven't already.


1. Open the **SmartThings mobile app**.
2. Navigate to **Routines**  and look for the **Discover** tab.
3. Scroll to the bottom; your new SmartApp will be listed under "My SmartApps".
4. Click the app to install it.
5. **Configuration:**
* Click on the SmartApp app which would start the installation, select your virtual switches.
* Select the corresponding **Blynk Pin** and enter the **Blynk Auth Token** for each switch.
* Hit **Save**.



You can now control your Blynk devices using the virtual switches integrated directly into your SmartThings ecosystem!

