// ignore_for_file: prefer_const_constructors, unused_import

import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:mictseta/Components/Buttons.dart';
import 'package:http/http.dart' as http;
import 'package:mictseta/Pages/MainPage.dart';
import '../Components/IconState.dart';
import '../Components/TextField.dart';
import 'CreateAccountPage.dart';

class Signuppage extends StatefulWidget {
  const Signuppage({super.key});

  @override
  State<Signuppage> createState() => _SignuppageState();
}

class _SignuppageState extends State<Signuppage> {
  TextEditingController emailController = TextEditingController();
  TextEditingController usernameController = TextEditingController();
  TextEditingController password1Controller = TextEditingController();
  TextEditingController password2Controller = TextEditingController();

  final storage = FlutterSecureStorage();
  Future<void> _sign_up(
      String email, String password1, String password2, String username) async {
    if (emailController.text.isEmpty &&
        password1Controller.text.isEmpty &&
        password2Controller.text.isEmpty &&
        usernameController.text.isEmpty) {
      showDialog(
          context: context,
          builder: (context) => AlertDialog(actions: [
                Buttons(
                  onTap: () {
                    Navigator.pop(context);
                  },
                  backgroundColor: Colors.white,
                  foregroundColor: const Color.fromARGB(255, 13, 72, 160),
                  child: 'Retry',
                ),
              ], content: Text('Please provide your credentials ')));
      return;
    } else if (email == 'admin@mictseta.com' ||
        email == 'humanresources@mictseta.com' ||
        email == 'manager@mictseta.com') {
      showDialog(
          context: context,
          builder: (context) => AlertDialog(
                  actions: [
                    Buttons(
                      onTap: () {
                        Navigator.pop(context);
                      },
                      backgroundColor: Colors.white,
                      foregroundColor: const Color.fromARGB(255, 13, 72, 160),
                      child: 'Okay',
                    ),
                  ],
                  content: Text(
                      'This credentials are not allowed on this platform.')));
      return;
    }
    showDialog(
        context: context,
        builder: (context) => Center(child: CircularProgressIndicator()));
    var url = 'http://10.0.2.2:8000/rest_api/auth/registration/';

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          "username": username,
          "email": email,
          "password1": password1,
          "password2": password2
        }),
      );

      if (response.statusCode == 200) {
        final responseData = jsonDecode(response.body);
        final token = responseData['key'];
        print(token);
        await storage.write(key: 'auth_token', value: token!);
        Navigator.push(
            context, MaterialPageRoute(builder: (context) => MainPage()));
      } else {
        Navigator.pop(context); 
      }
    } catch (e) {
      Navigator.pop(context);
      print('Error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blue[100],
      appBar: AppBar(
        title: Text('Create an account'),
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
                keyBoardType: TextInputType.emailAddress,
                icon: Icons.mail,
                state: false,
                controller: emailController,
                hintText: 'Enter your email',
              ),
              TextfieldPage(
                keyBoardType: TextInputType.name,
                icon: Icons.person,
                state: false,
                controller: usernameController,
                hintText: 'Enter your username',
              ),
              TextfieldPage(
                keyBoardType: TextInputType.name,
                icon: Icons.password,
                state: true,
                controller: password1Controller,
                hintText: 'Enter your password',
              ),
              TextfieldPage(
                keyBoardType: TextInputType.name,
                icon: Icons.password,
                state: true,
                controller: password2Controller,
                hintText: 're-enter your password',
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
                  _sign_up(emailController.text, password1Controller.text,
                      password2Controller.text, usernameController.text);
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
                  'Register',
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
