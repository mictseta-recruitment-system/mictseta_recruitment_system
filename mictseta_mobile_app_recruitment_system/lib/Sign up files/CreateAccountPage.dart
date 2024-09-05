import 'dart:convert';

import 'package:flutter/material.dart'; 
import 'package:http/http.dart' as http;

class Createaccountpage extends StatefulWidget {
  final String name;
  final String surname;
  final int idNumber;
  const Createaccountpage(
      {super.key,
      required this.name,
      required this.surname,
      required this.idNumber});

  @override
  State<Createaccountpage> createState() => _CreateaccountpageState();
}

class _CreateaccountpageState extends State<Createaccountpage> {
  TextEditingController emailController = TextEditingController();
  TextEditingController passwordController = TextEditingController();
  TextEditingController confirmPasswordController = TextEditingController();
  
  Future<void> signUpUser(String name, String surname, String idNumber,
      String password, String password2) async {
    if (password != password2) {
      print('Passwords do not match.');
      return;
    }

    var url = Uri.parse('http://127.0.0.1:8000/auth/sign_up/');

    var data = {
      "username": name,
      "email": surname,
      "idnumber": idNumber,
      "password": password,
      "password2": password2,
    };

    try {
      var response = await http.post(
        url,
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(data),
      );

      if (response.statusCode == 200) {
        print('User signed up successfully.');
      } else {
        print('Failed to sign up user. Status code: ${response.statusCode}');
      }
    } catch (e) {
      print('Error signing up user: $e');
    }
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Account Details'),
        centerTitle: true,
        backgroundColor: Colors.blue[900],
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: const EdgeInsets.all(10.0),
        child: SingleChildScrollView(
            child: Column(
          children: [
            // Iconstate(icon: Icons.person_add_alt_1_outlined),
            // SizedBox(height: 20),
            // TextfieldPage(
            //   keyBoardType: TextInputType.emailAddress,
            //   icon: Icons.mail_lock_outlined,
            //   state: false,
            //   controller: emailController,
            //   hintText: 'Enter your Email',
            // ),
            // TextfieldPage(
            //   keyBoardType: TextInputType.visiblePassword,
            //   icon: Icons.password,
            //   state: true,
            //   controller: emailController,
            //   hintText: 'Password',
            // ),
            // TextfieldPage(
            //   keyBoardType: TextInputType.visiblePassword,
            //   icon: Icons.password,
            //   state: true,
            //   controller: emailController,
            //   hintText: 'Confirm Password',
            // ),
            // SizedBox(
            //   height: 10,
            // ),
            // OutlinedButton(
            //   onPressed: () {},
            //   style: ButtonStyle(
            //     minimumSize: WidgetStatePropertyAll(
            //       Size(double.infinity, 60),
            //     ),
            //     foregroundColor: WidgetStatePropertyAll(Colors.blue[50]),
            //     backgroundColor: WidgetStatePropertyAll(Colors.blue[900]),
            //     shape: WidgetStatePropertyAll(RoundedRectangleBorder(
            //         borderRadius: BorderRadius.circular(5))),
            //     side: WidgetStateProperty.resolveWith<BorderSide>(
            //       (Set<WidgetState> states) {
            //         return BorderSide(
            //           color: const Color.fromARGB(255, 11, 66, 148),
            //           width: 1,
            //         );
            //       },
            //     ),
            //   ),
            //   child: Text(
            //     'Create Account',
            //   ),
            // ),
          ],
        )),
      ),
    );
  }
}
