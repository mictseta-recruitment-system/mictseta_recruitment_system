import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'package:mictseta/Components/Buttons.dart';
import 'package:mictseta/Components/Card.dart';
import 'package:mictseta/Pages/ProfileInformation.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  String? token;
  final storage = const FlutterSecureStorage();
  Map<String, dynamic>? profileData;
  bool isLoading = true;
  String error = '';

  @override
  void initState() {
    super.initState();
    _retrieveTokenAndUser();
  }

  Future<void> _retrieveTokenAndUser() async {
    String? tkn = await storage.read(key: 'auth_token');
    if (tkn != null) {
      setState(() {
        token = tkn;
      });
      await getLoggedInUser(tkn);
    } else {
      setState(() {
        isLoading = false;
        error = 'No token found';
      });
    }
  }

  Future<void> getLoggedInUser(String token) async {
    final String url = 'http://127.0.0.1:8000/rest_api/user/';

    try {
      final response = await http.get(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Token $token',
        },
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> userData = jsonDecode(response.body);
        await getUserProfile(userData['id'], token);
      } else {
        setState(() {
          error =
              'Failed to retrieve user. Status code: ${response.statusCode}';
          isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        error = 'Error: $e';
        isLoading = false;
      });
    }
  }

  Future<void> getUserProfile(int id, String token) async {
    final String url = 'http://127.0.0.1:8000/rest_api/profile/';

    try {
      final response = await http.get(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Token $token',
        },
      );

      if (response.statusCode == 200) {
        print('User\'s Profile data: ${jsonDecode(response.body)}');
        setState(() {
          profileData = jsonDecode(response.body);
          isLoading = false;
        });
      } else {
        setState(() {
          error = 'Failed to load profile. Status code: ${response.statusCode}';
          isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        error = 'Error: $e';
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : error.isNotEmpty
              ? Center(child: Text('Error: $error'))
              : profileData != null
                  ? Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          ProfileCard(
                            widget: profileData!['profile_image'] != null
                                ? ClipRRect(
                                    borderRadius: BorderRadius.circular(50),
                                    child: Image.network(
                                        profileData!['profile_image'],
                                        height: 100,
                                        width: 100,
                                        fit: BoxFit.cover))
                                : ClipRRect(
                                    borderRadius: BorderRadius.circular(75),
                                    child: Image.asset(
                                        'assets/Male_empty_profile.png',
                                        height: 100,
                                        width: 100,
                                        fit: BoxFit.cover)),
                            name: profileData!['name'],
                            surname: profileData!['surname'],
                            dateOfBirth: profileData!['dob'],
                            phoneNumber: profileData!['phone'],
                          ),
                          SizedBox(height:20),
                          Buttons(
                            backgroundColor: Colors.blue,
                            foregroundColor: Colors.white,
                            child:'Update Profile',
                            onTap:(){
                              Navigator.push(context, MaterialPageRoute(builder: (context)=>ProfileInformation(userData: profileData!,)));
                            }
                          )

                          // Text(
                          //     'Marital Status: ${profileData!['maritial_status']}'),
                          // Text('Race: ${profileData!['race']}'),
                          // Text('Disability: ${profileData!['disability']}'),
                          // Text('Verified: ${profileData!['is_verified']}'),
                          // Text(
                          //     'LinkedIn Profile: ${profileData!['linkedin_profile']}'),
                          // Text(
                          //     'Personal Website: ${profileData!['personal_website']}'),
                          // Text(
                          //     'Qualifications: ${profileData!['qualifications']}'),
                          // Text('Languages: ${profileData!['languages']}'),
                          // Text(
                          //     'Computer Skills: ${profileData!['computer_skills']}'),
                          // Text('Soft Skills: ${profileData!['soft_skills']}'),
                          // Text(
                          //     'Work Experience: ${profileData!['working_experience']}'),
                          // Text(
                          //     'Address Information: ${profileData!['address_information']}'),
                        ],
                      ),
                    )
                  : const Center(child: Text('No profile found')),
    );
  }
}
