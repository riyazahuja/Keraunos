const noble = require('noble');

const SERVICE_UUID = '12345678-1234-5678-1234-56789abcdef0';
const CHARACTERISTIC_UUID = '12345678-1234-5678-1234-56789abcdef1';

noble.on('stateChange', function (state) {
  if (state === 'poweredOn') {
    console.log('Scanning...');
    noble.startScanning([SERVICE_UUID], false);
  } else {
    noble.stopScanning();
  }
});

noble.on('discover', function (peripheral) {
  console.log(`Found device with local name: ${peripheral.advertisement.localName}`);
  console.log(`advertising the following service uuid's: ${peripheral.advertisement.serviceUuids}`);
  console.log();

  peripheral.connect(function (error) {
    console.log('Connected to', peripheral.id);

    peripheral.discoverServices([SERVICE_UUID], function (error, services) {
      var service = services[0];
      console.log('Discovered service', service.uuid);

      service.discoverCharacteristics([], function (error, characteristics) {
        console.log('Discovered characteristics');

        var characteristic = characteristics.find(c => c.uuid === CHARACTERISTIC_UUID);
        characteristic.read(function (error, data) {
          if (data) {
            console.log(`Read: ${data.toString('utf8')}`);
          }
          peripheral.disconnect();
        });
      });
    });
  });
});
