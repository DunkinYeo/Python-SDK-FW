package com.wellysis.sdkautotester;

import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCharacteristic;

/**
 * GattListener interface - a top-level interface that pyjnius PythonJavaClass can implement.
 *
 * The GattCallbackWrapper (which extends the abstract BluetoothGattCallback class)
 * delegates all callbacks to this interface. This is necessary because:
 *
 * 1. jnius PythonJavaClass can only implement interfaces, not abstract classes
 * 2. We need to bridge Python code with the Android BluetoothGattCallback
 * 3. This interface is standalone (not an inner class) for cleaner jnius binding
 */
public interface GattListener {
    void onConnectionStateChange(BluetoothGatt gatt, int status, int newState);
    void onServicesDiscovered(BluetoothGatt gatt, int status);
    void onCharacteristicRead(BluetoothGatt gatt, BluetoothGattCharacteristic c, int status);
    void onCharacteristicWrite(BluetoothGatt gatt, BluetoothGattCharacteristic c, int status);
    void onCharacteristicChanged(BluetoothGatt gatt, BluetoothGattCharacteristic c);
}
