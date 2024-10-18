import 'package:flutter/material.dart';

class ProfileCard extends StatelessWidget {
  final String name;
  final String surname;
  final String dateOfBirth;
  final String phoneNumber;
  final Widget widget;
  const ProfileCard(
      {super.key,
      required this.name,
      required this.surname,
      required this.dateOfBirth,
      required this.phoneNumber,
      required this.widget});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 200,
      decoration: BoxDecoration(
          border: Border.all(color: Colors.blue),
          borderRadius: BorderRadius.circular(20)),
      child: Padding(
        padding: const EdgeInsets.all(10.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            ClipRRect(borderRadius: BorderRadius.circular(75), child: widget),
            Container(
              child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text('$name $surname',
                        style: TextStyle(
                            fontSize: 18,
                            fontFamily: 'Roboto',
                            fontWeight: FontWeight.bold),overflow:TextOverflow.ellipsis),
                    Text(phoneNumber,
                        style: TextStyle(
                            fontSize: 18,
                            fontFamily: 'Roboto',
                            fontWeight: FontWeight.bold),overflow:TextOverflow.ellipsis),
                    Text(dateOfBirth,
                        style: TextStyle(
                            fontSize: 18,
                            fontFamily: 'Roboto',
                            fontWeight: FontWeight.bold),overflow:TextOverflow.ellipsis),
                  ]),
            )
          ],
        ),
      ),
    );
  }
}
