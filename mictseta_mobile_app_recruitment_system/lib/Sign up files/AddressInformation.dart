import 'package:flutter/material.dart';
import 'package:geocoding/geocoding.dart';
import 'package:geolocator/geolocator.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:permission_handler/permission_handler.dart';

import '../Components/IconState.dart';
import '../Components/TextField.dart';

class AddressInformation extends StatefulWidget {
  const AddressInformation({super.key});

  @override
  State<AddressInformation> createState() => _AddressInformationState();
}

class _AddressInformationState extends State<AddressInformation> {
  TextEditingController address1Controller = TextEditingController();
  TextEditingController address2Controller = TextEditingController();
  TextEditingController cityController = TextEditingController();
  TextEditingController streetController = TextEditingController();
  TextEditingController postalCodeController = TextEditingController();
  TextEditingController provinceController = TextEditingController();

  late LatLng currentLocation;

  @override
  void initState() {
    super.initState();
    requestLocationPermission();
  }

  Future<void> getCurrentLocation() async {
    try {
      List<Location> locations = await locationFromAddress(
        'address',
      );
      if (locations.isNotEmpty) {
        List<Placemark> placemarks = await placemarkFromCoordinates(
          locations.first.latitude,
          locations.first.longitude,
        );

        if (placemarks.isNotEmpty) {
          setState(() {
            currentLocation = LatLng(
              locations.first.latitude,
              locations.first.longitude,
            );
          });

          // txtLiveLocation.text = placemarks.first.street ?? '';
        } else {
          print('Placemark not found');
        }
      } else {
        print('Location not found');
      }
    } catch (e) {
      print('Error: $e');
    }
  }

  Future<void> showLocationDialog(BuildContext context) async {
    LocationPermission permission = await Geolocator.requestPermission();
    if (permission == LocationPermission.denied) {
      getCurrentLocation();
      print('Location permission denied');
      return;
    }

    Position position = await Geolocator.getCurrentPosition();

    try {
      List<Placemark> placemarks =
          await placemarkFromCoordinates(position.latitude, position.longitude);

      Navigator.of(context).pop();
      if (placemarks.isNotEmpty) {
        String city = placemarks.first.subLocality ?? 'Unknown';
        String postalCode = placemarks.first.postalCode ?? 'Unknown';
        String street = placemarks.first.street ?? 'Unknown';
        String address1 = placemarks.first.subThoroughfare ?? 'Unknown';

        cityController.text = city;
        streetController.text = street;
        postalCodeController.text = postalCode;
        address1Controller.text = address1;
      }
    } catch (e) {
      print('Error fetching address: $e');
    }
  }

  Future<void> requestLocationPermission() async {
    var status = await Permission.location.request();
    if (status == PermissionStatus.granted) {
      getCurrentLocation();
    } else {
      print('Location permission denied');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blue[100],
      appBar: AppBar(
        title: Text('Address information'),
        backgroundColor: Colors.blue[900],
        foregroundColor: Colors.white,
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(10.0),
        child: Column(
          children: [
            Iconstate(icon: Icons.location_on_outlined),
            SizedBox(
              height: 10,
            ),
            TextfieldPage2(
              keyBoardType: TextInputType.streetAddress,
              controller: address1Controller,
              hintText: 'Address line 1',
            ),
            TextfieldPage2(
              keyBoardType: TextInputType.streetAddress,
              controller: address2Controller,
              hintText: 'Address line 2',
            ),
            TextfieldPage2(
              keyBoardType: TextInputType.text,
              controller: cityController,
              hintText: 'City',
            ),
            TextfieldPage2(
              keyBoardType: TextInputType.number,
              controller: postalCodeController,
              hintText: 'Postal code',
            ),
            TextfieldPage2(
              keyBoardType: TextInputType.text,
              controller: streetController,
              hintText: 'Street e.g st 23',
            ),
          ],
        ),
      ),
    );
  }
}
