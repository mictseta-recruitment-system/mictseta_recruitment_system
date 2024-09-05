// ignore_for_file: prefer_const_literals_to_create_immutables, prefer_const_constructors

import 'package:flutter/material.dart';

import '../Components/ExpansionChoose.dart';
import '../Components/IconState.dart';


class ExperienceInformation extends StatefulWidget {
  const ExperienceInformation({super.key});

  @override
  State<ExperienceInformation> createState() => _ExperienceInformationState();
}

class _ExperienceInformationState extends State<ExperienceInformation> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blue[100],
      appBar: AppBar(
        title: Text('Education Information'),
        backgroundColor: Colors.blue[900],
        foregroundColor: Colors.white,
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(10.0),
        child: Column(
          children: [
            Iconstate(icon: Icons.volunteer_activism_outlined),
            SizedBox(
              height: 10,
            ),
            ExpansionTileChoose(
              selectedValue: 'Select Department',
              valueS: [
                'Advertising',
                'Electronics',
                'Film and Electronic Media',
                'Information Technology',
                'Telecommunications'
              ],
            ),
            ExpansionTileChoose(
              selectedValue: 'Select Department',
              valueS: [
                'Advertising',
                'Electronics',
                'Film and Electronic Media',
                'Information Technology',
                'Telecommunications'
              ],
            ),
            ExpansionTileChoose(
              selectedValue: 'Select Department',
              valueS: [
                'Advertising',
                'Electronics',
                'Film and Electronic Media',
                'Information Technology',
                'Telecommunications'
              ],
            ),
            ExpansionTileChoose(
              selectedValue: 'Select Department',
              valueS: [
                'Advertising',
                'Electronics',
                'Film and Electronic Media',
                'Information Technology',
                'Telecommunications'
              ],
            ),
            ExpansionTileChoose(
              selectedValue: 'Select Department',
              valueS: [
                'Advertising',
                'Electronics',
                'Film and Electronic Media',
                'Information Technology',
                'Telecommunications'
              ],
            ),
          ],
        ),
      ),
    );
  }
}
