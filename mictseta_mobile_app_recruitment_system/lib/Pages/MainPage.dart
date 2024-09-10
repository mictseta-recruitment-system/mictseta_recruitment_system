// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables, prefer_final_fields

import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'MICSETAFeedback.dart';
import 'ProfilePage.dart';
import 'home-page.dart';
import 'more_information_page.dart';
import 'notificationPage.dart';

class MainPage extends StatefulWidget {
  final String? token;
  const MainPage({
    super.key,
    required this.token,
  });

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  int _selectedIndex = 0;

  void openFeedBack() {
    Navigator.of(context).pop();
    Navigator.push(
        context, MaterialPageRoute(builder: (context) => FeedBackPage()));
  }

  List<Widget> _widgetOptions = [HomePage(), Notificationpage(), Profilepage()];
  
  
  void _log_out(String token) async {
   
    showDialog(
        context: context,
        builder: (context) => Center(child: CircularProgressIndicator()));
    var url = 'http://10.0.2.2:8000/rest_api/auth/log-out/';

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json', 'Authorization':'Bearer $token'},
        body: jsonEncode({}),
      );

      if (response.statusCode == 200) {
        Navigator.pop(context);
        Navigator.pop(context);
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
      appBar: AppBar(
        title: Text('Welcome to MICSETA'),
        backgroundColor: Colors.blue[900],
        foregroundColor: Colors.white,
        centerTitle: true,
      ),
      drawer: Drawer(
        backgroundColor: Colors.blue[900],
        child: Padding(
          padding: const EdgeInsets.all(10.0),
          child: ListView(
            children: <Widget>[
              Text(
                'More Information',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                ),
              ),
              Icon(
                Icons.mood_rounded,
                size: 150,
                color: Colors.white,
              ),
              SizedBox(
                height: 20,
              ),
              ListTile(
                leading: Icon(
                  Icons.info_outlined,
                  color: Colors.white,
                ),
                title: Text('About Us', style: TextStyle(color: Colors.white)),
                onTap: () {
                  Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (context) => MoreInformationPage(
                                tabName: 'About Us',
                              )));
                },
              ),
              ListTile(
                leading: Icon(
                  Icons.contact_page,
                  color: Colors.white,
                ),
                title:
                    Text('Contact Us', style: TextStyle(color: Colors.white)),
                onTap: () {
                  Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (context) => MoreInformationPage(
                                tabName: 'Contact Us',
                              )));
                },
              ),
              ListTile(
                leading: Icon(
                  Icons.question_mark_outlined,
                  color: Colors.white,
                ),
                title: Text('Help', style: TextStyle(color: Colors.white)),
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (context) => MoreInformationPage(
                              tabName: 'Help Center',
                            )),
                  );
                },
              ),
              ListTile(
                leading: Icon(
                  Icons.logout_outlined,
                  color: Colors.white,
                ),
                title: Text('Log Out', style: TextStyle(color: Colors.white)),
                onTap: () {
                  _log_out(widget.token!);
                },
              ),
            ],
          ),
        ),
      ),
      body: _widgetOptions[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        backgroundColor: Colors.blue[900],
        useLegacyColorScheme: true,
        unselectedItemColor: Colors.grey,
        items: <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(
              Icons.home,
            ),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.notifications),
            label: 'Notification',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.account_circle),
            label: 'Profile',
          ),
        ],
        currentIndex: _selectedIndex,
        selectedItemColor: Colors.white,
        onTap: _onItemTapped,
      ),
    );
  }

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
      // _token=widget.token!;
    });
  }
}
