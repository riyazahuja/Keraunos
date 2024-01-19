const bleno = require('bleno');

const SERVICE_UUID = '12345678-1234-5678-1234-56789abcdef0';
const CHARACTERISTIC_UUID = '12345678-1234-5678-1234-56789abcdef1';

class HelloCharacteristic extends bleno.Characteristic {
  constructor() {
    super({
      uuid: CHARACTERISTIC_UUID,
      properties: ['read'],
      value: null,
    });

    this._value = Buffer.from('Hello!');
  }

  onReadRequest(offset, callback) {
    console.log('Read request received');
    callback(this.RESULT_SUCCESS, this._value.slice(offset, this._value.length));
  }
}

bleno.on('stateChange', function (state) {
  console.log(`State change: ${state}`);
  if (state === 'poweredOn') {
    bleno.startAdvertising('HelloPeripheral', [SERVICE_UUID]);
  } else {
    bleno.stopAdvertising();
  }
});

bleno.on('advertisingStart', function (error) {
  console.log('Advertising start: ' + (error ? 'error ' + error : 'success'));
  if (!error) {
    bleno.setServices([
      new bleno.PrimaryService({
        uuid: SERVICE_UUID,
        characteristics: [
          new HelloCharacteristic(),
        ],
      }),
    ]);
  }
});
