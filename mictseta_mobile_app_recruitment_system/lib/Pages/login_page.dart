// ignore_for_file: sized_box_for_whitespace, prefer_const_constructors, prefer_const_literals_to_create_immutables

import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:mictseta_mobile_app_recruitment_system/Components/Buttons.dart';

import 'MainPage.dart';
import '../Sign up files/SignUpPage.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  TextEditingController passwordController = TextEditingController();
  TextEditingController emailController = TextEditingController();
  Future<void> _sign_in(String email, String password) async {
    if (emailController.text.isEmpty && passwordController.text.isEmpty) {
      showDialog(
          context: context,
          builder: (context) => AlertDialog(actions: [
                Buttons(
                  onTap: () {
                    Navigator.pop(context);
                  },
                  backgroundColor: Colors.white,
                  foregroundColor: const Color.fromARGB(255, 13, 72, 160),
                  child: '',
                ),
              ], content: Text('Please provide your credentials ')));
      return;
    }
    showDialog(
        context: context,
        builder: (context) => Center(child: CircularProgressIndicator()));
    var url = 'http://10.0.2.2:8000/rest_api/auth/sign-in/';

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
          
        },
        body: jsonEncode({"email": email, "password": password}),
      );

      if (response.statusCode == 200) {
        var data = jsonDecode(response.body);
        print(data['token']);
        Navigator.push(
            context, MaterialPageRoute(builder: (context) => MainPage()));
      } else {
        Navigator.pop(context);
        print('Failed to apply: ${response.statusCode}');
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
      body: Padding(
        padding: const EdgeInsets.all(10.0),
        child: SingleChildScrollView(
          scrollDirection: Axis.vertical,
          child: Column(
            children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(125),
                child: Image.asset(
                  'assets/image.png',
                  height: 250,
                  width: 250,
                  fit: BoxFit.cover,
                ),
              ),
              SizedBox(
                height: 10,
              ),
              Container(
                decoration: BoxDecoration(
                  border: Border.all(
                    color: Colors.blue,
                    width: 1.0,
                  ),
                  borderRadius: BorderRadius.circular(5.0),
                ),
                child: TextField(
                  controller: emailController,
                  decoration: InputDecoration(
                    labelText: 'Enter your email',
                    border: InputBorder.none,
                    contentPadding: EdgeInsets.symmetric(horizontal: 20.0),
                  ),
                ),
              ),
              SizedBox(
                height: 5,
              ),
              Container(
                decoration: BoxDecoration(
                  border: Border.all(
                    color: Colors.blue,
                    width: 1.0,
                  ),
                  borderRadius: BorderRadius.circular(5.0),
                ),
                child: TextField(
                  obscureText: true,
                  controller: passwordController,
                  decoration: InputDecoration(
                    labelText: 'Enter your Password',
                    border: InputBorder.none,
                    contentPadding: EdgeInsets.symmetric(horizontal: 20.0),
                  ),
                ),
              ),
              SizedBox(
                height: 5,
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  Text(
                    'Forgot password?',
                    style: TextStyle(color: Colors.blue),
                  ),
                ],
              ),
              SizedBox(
                height: 10,
              ),
              OutlinedButton(
                onPressed: () {
                  _sign_in(emailController.text, passwordController.text);
                },
                style: ButtonStyle(
                  minimumSize: WidgetStatePropertyAll(
                    Size(double.infinity, 55),
                  ),
                  foregroundColor: WidgetStatePropertyAll(Colors.blue[50]),
                  backgroundColor: WidgetStatePropertyAll(Colors.blue[900]),
                  shape: WidgetStatePropertyAll(RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(5))),
                  side: WidgetStateProperty.resolveWith<BorderSide>(
                    (Set<WidgetState> states) {
                      return BorderSide(
                        color: const Color.fromARGB(255, 14, 74, 165),
                        width: 1.0,
                      );
                    },
                  ),
                ),
                child: Text(
                  'Sign in',
                ),
              ),
              SizedBox(
                height: 5,
              ),
              OutlinedButton(
                onPressed: () {
                  print('in the next page');
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => MainPage()),
                  );
                },
                style: ButtonStyle(
                  minimumSize: WidgetStatePropertyAll(
                    Size(double.infinity, 55),
                  ),
                  foregroundColor: WidgetStatePropertyAll(Colors.blue[900]),
                  backgroundColor: WidgetStatePropertyAll(Colors.blue[50]),
                  shape: WidgetStatePropertyAll(RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(5))),
                  side: WidgetStateProperty.resolveWith<BorderSide>(
                    (Set<WidgetState> states) {
                      return BorderSide(
                        color: const Color.fromARGB(255, 13, 73, 163),
                        width: 2.0,
                      );
                    },
                  ),
                ),
                child: Text('Continue without login'),
              ),
              SizedBox(
                height: 10,
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Expanded(child: Divider()),
                  Text('Or'),
                  Expanded(child: Divider())
                ],
              ),
              GestureDetector(
                onTap: () {
                  Navigator.push(context,
                      MaterialPageRoute(builder: (context) => Signuppage()));
                },
                child: Text(
                  'Create an account',
                  style: TextStyle(color: Colors.blue[900], fontSize: 17),
                ),
              ),
              SizedBox(
                height: 40,
              )
            ],
          ),
        ),
      ),
    );
  }
}
