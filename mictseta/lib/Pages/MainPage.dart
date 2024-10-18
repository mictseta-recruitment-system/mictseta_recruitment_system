import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'notificationPage.dart';
import 'ProfilePage.dart';
import 'home-page.dart';
import 'more_information_page.dart';

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  int _selectedIndex = 0;
  String? token;
  final storage = FlutterSecureStorage();
  final List<Widget> _screens = [HomePage(), Notificationpage(), ProfilePage()];

  @override
  void initState() {
    super.initState();
    _retrieveToken();
  }

  Future<void> _retrieveToken() async {
    try {
      final String? tkn = await storage.read(key: 'auth_token');
      if (tkn != null) {
        setState(() {
          token = tkn;
        });
      } else {
        print('No token found');
      }
    } catch (e) {
      print('Error retrieving token: $e');
    }
  }

  Future<void> _log_out() async {
    showDialog(
      context: context,
      builder: (context) => Center(child: CircularProgressIndicator()),
    );

    final url = 'http://10.0.2.2:8000/rest_api/auth/logout/';
    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Token $token',
        },
        body: jsonEncode({}),
      );

      Navigator.pop(context); // Close the dialog
      if (response.statusCode == 200) {
        Navigator.popUntil(context,
            (route) => route.isFirst); // Navigate to home or initial page
      } else {
        print('Failed to logout: ${response.statusCode}');
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to logout')),
        );
      }
    } catch (e) {
      Navigator.pop(context); // Close the dialog
      print('Error: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error logging out')),
      );
    }
  }

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
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
              SizedBox(height: 20),
              ListTile(
                leading: Icon(Icons.info_outlined, color: Colors.white),
                title: Text('About Us', style: TextStyle(color: Colors.white)),
                onTap: () => Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) =>
                        MoreInformationPage(tabName: 'About Us'),
                  ),
                ),
              ),
              ListTile(
                leading: Icon(Icons.contact_page, color: Colors.white),
                title:
                    Text('Contact Us', style: TextStyle(color: Colors.white)),
                onTap: () => Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) =>
                        MoreInformationPage(tabName: 'Contact Us'),
                  ),
                ),
              ),
              ListTile(
                leading:
                    Icon(Icons.question_mark_outlined, color: Colors.white),
                title: Text('Help', style: TextStyle(color: Colors.white)),
                onTap: () => Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) =>
                        MoreInformationPage(tabName: 'Help Center'),
                  ),
                ),
              ),
              ListTile(
                leading: Icon(Icons.logout_outlined, color: Colors.white),
                title: Text('Log Out', style: TextStyle(color: Colors.white)),
                onTap: _log_out,
              ),
            ],
          ),
        ),
      ),
      body: _screens[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        backgroundColor: Colors.blue[900],
        unselectedItemColor: Colors.grey,
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
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
}
