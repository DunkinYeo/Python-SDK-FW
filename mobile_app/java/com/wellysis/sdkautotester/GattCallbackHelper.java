package com.wellysis.sdkautotester;

import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

/**
 * Pure-Java GATT callback helper.
 * Extends BluetoothGattCallback directly — no Python interface needed.
 * Python polls the state fields instead of using PythonJavaClass callbacks.
 */
public class GattCallbackHelper extends BluetoothGattCallback {

    private final AtomicInteger  connectionState     = new AtomicInteger(-1);
    private final AtomicBoolean  servicesDiscovered  = new AtomicBoolean(false);

    private final AtomicBoolean  readDone  = new AtomicBoolean(false);
    private final AtomicBoolean  readOk    = new AtomicBoolean(false);
    private final AtomicReference<byte[]> readValue  = new AtomicReference<>(null);

    private final AtomicBoolean  writeDone = new AtomicBoolean(false);
    private final AtomicBoolean  writeOk   = new AtomicBoolean(false);

    private final LinkedBlockingQueue<byte[]> notifyQueue = new LinkedBlockingQueue<>();

    // ── BluetoothGattCallback overrides ──────────────────────────────────────

    @Override
    public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState) {
        connectionState.set(newState);
        if (newState == 2) {   // BluetoothProfile.STATE_CONNECTED
            gatt.discoverServices();
        }
    }

    @Override
    public void onServicesDiscovered(BluetoothGatt gatt, int status) {
        if (status == 0) servicesDiscovered.set(true);
    }

    @Override
    public void onCharacteristicRead(BluetoothGatt gatt,
                                     BluetoothGattCharacteristic c, int status) {
        readOk.set(status == 0);
        byte[] val = c.getValue();
        readValue.set((status == 0 && val != null) ? val.clone() : null);
        readDone.set(true);
    }

    @Override
    public void onCharacteristicWrite(BluetoothGatt gatt,
                                      BluetoothGattCharacteristic c, int status) {
        writeOk.set(status == 0);
        writeDone.set(true);
    }

    @Override
    public void onCharacteristicChanged(BluetoothGatt gatt,
                                        BluetoothGattCharacteristic c) {
        byte[] val = c.getValue();
        if (val != null) notifyQueue.offer(val.clone());
    }

    // ── Python-callable getters / actions ─────────────────────────────────────

    public int     getConnectionState()    { return connectionState.get(); }
    public boolean isServicesDiscovered()  { return servicesDiscovered.get(); }

    public boolean isReadDone()  { return readDone.get(); }
    public boolean isReadOk()    { return readOk.get(); }
    public byte[]  getReadValue(){ return readValue.get(); }
    public void    clearRead()   { readDone.set(false); readOk.set(false); readValue.set(null); }

    public boolean isWriteDone() { return writeDone.get(); }
    public boolean isWriteOk()   { return writeOk.get(); }
    public void    clearWrite()  { writeDone.set(false); writeOk.set(false); }

    /** Block up to timeoutMs for the next notification packet, or return null. */
    public byte[] pollNotify(long timeoutMs) throws InterruptedException {
        return notifyQueue.poll(timeoutMs, TimeUnit.MILLISECONDS);
    }
    public void clearNotify() { notifyQueue.clear(); }
}
