// ignore_for_file: prefer_const_constructors, unused_import

import 'dart:convert';

import 'package:flutter/material.dart';

import '../Components/IconState.dart';
import '../Components/TextField.dart';
import 'CreateAccountPage.dart';

class Signuppage extends StatefulWidget {
  const Signuppage({super.key});

  @override
  State<Signuppage> createState() => _SignuppageState();
}

class _SignuppageState extends State<Signuppage> {
  TextEditingController nameController = TextEditingController();
  TextEditingController surnameController = TextEditingController();
  TextEditingController cellPhoneController = TextEditingController();
  TextEditingController idNumberController = TextEditingController();

  String phoneNumber = '';
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blue[100],
      appBar: AppBar(
        title: Text('Personal Information'),
        centerTitle: true,
        foregroundColor: Colors.white,
        backgroundColor: Colors.blue[900],
      ),
      body: Padding(
        padding: const EdgeInsets.all(10.0),
        child: SingleChildScrollView(
          child: Column(
            children: [
              Iconstate(icon: Icons.person),
              SizedBox(
                height: 20,
              ),
              TextfieldPage(
                keyBoardType: TextInputType.name,
                icon: Icons.person,
                state: false,
                controller: nameController,
                hintText: 'Enter your Name',
              ),
              TextfieldPage(
                keyBoardType: TextInputType.name,
                icon: Icons.person,
                state: false,
                controller: surnameController,
                hintText: 'Enter your Surname',
              ),
              TextfieldPage(
                keyBoardType: TextInputType.number,
                icon: Icons.person,
                state: false,
                controller: idNumberController,
                hintText: 'Enter your Id Number',
              ),
              // IntlPhoneField(
              //                 decoration: InputDecoration(
              // labelText: 'Phone Number',
              // border: OutlineInputBorder(
              //   borderSide: BorderSide(
              //       color: const Color.fromARGB(255, 14, 75, 165)),
              //   borderRadius: BorderRadius.circular(10),
              // ),
              // focusedBorder: OutlineInputBorder(
              //   borderSide: BorderSide(
              //       color: const Color.fromARGB(255, 13, 73, 163)),
              //   borderRadius: BorderRadius.circular(10),
              // ),
              //                 ),
              //                 initialCountryCode: 'ZA',
              //                 onChanged: (phone) {
              // setState(() {
              //   phoneNumber = phone.completeNumber;
              // });
              //                 },
              //                 controller: cellPhoneController,
              //               ),
              OutlinedButton(
                onPressed: () {
                  
                  Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (context) => Createaccountpage(
                              name: nameController.text,
                              surname: surnameController.text,
                              idNumber: int.parse(idNumberController.text))));
                },
                style: ButtonStyle(
                  minimumSize: WidgetStatePropertyAll(
                    Size(double.infinity, 60),
                  ),
                  foregroundColor: WidgetStatePropertyAll(Colors.blue[900]),
                  backgroundColor: WidgetStatePropertyAll(Colors.blue[50]),
                  shape: WidgetStatePropertyAll(RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(5))),
                  side: WidgetStateProperty.resolveWith<BorderSide>(
                    (Set<WidgetState> states) {
                      return BorderSide(
                        color: const Color.fromARGB(255, 11, 66, 148),
                        width: 1,
                      );
                    },
                  ),
                ),
                child: Text(
                  'Next',
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
