// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';

import 'MICSETAFeedback.dart';

class Notificationpage extends StatelessWidget {
  const Notificationpage({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(10.0),
      child: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Notification',
              style: TextStyle(fontSize: 19, fontWeight: FontWeight.bold),
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
          borderRadius: BorderRadius.circular(10.0),
        ),
              child: ListTile(
                leading: Image.asset('assets/image.png'),
                title: Text('MICSETA feedback',style:TextStyle(
              fontSize: 15,
              fontWeight: FontWeight.bold,
            ),
            overflow: TextOverflow.ellipsis,
            maxLines: 1,),
                subtitle: Text(
                    'Hi we regret to inform you that your application went unsuccessful.',style:TextStyle(
),
            overflow: TextOverflow.ellipsis,
            maxLines: 1,),
                trailing: Icon(Icons.arrow_right_outlined,color:Colors.blue[900],size: 30,),
                onTap: () {
                  Navigator.push(context,
                      MaterialPageRoute(builder: (context) => FeedBackPage()));
                },
              ),
            )
          ],
        ),
      ),
    );
  }
}
