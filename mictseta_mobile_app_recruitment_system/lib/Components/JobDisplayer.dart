// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';

class JobdisplayerPage extends StatelessWidget {
  // final String imageUrl;
  // final IconData icon;
  final String jobTitle;
  final String jobDescription;

  final String jobDue;
  final String date;
  final Function onTap;
  final String location;

  const JobdisplayerPage({
    super.key,
    required this.jobTitle,
    required this.jobDescription,
    required this.location,
    required this.jobDue,
    required this.date, required this.onTap,
    // required this.icon
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        decoration: BoxDecoration(
          border: Border.all(
            color: Colors.blue,
            width: 1.0,
          ),
          borderRadius: BorderRadius.circular(10.0),
        ),
        child: Expanded(
            child: ListTile(
          title: Text(
            jobTitle,
            style: TextStyle(
              fontSize: 15,
              fontWeight: FontWeight.bold,
            ),
            overflow: TextOverflow.ellipsis,
            maxLines: 1,
          ),
          subtitle: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                jobDescription,
                style: TextStyle(fontSize: 15, fontWeight: FontWeight.w300),
                overflow: TextOverflow.ellipsis,
                maxLines: 1,
              ),
              Row(children: [
                Row(
                  children: [
                    Icon(
                      Icons.lock_clock,
                      size: 16,
                      color: Colors.blue[900],
                    ),
                    Text(
                      jobDue,
                      overflow: TextOverflow.ellipsis,
                      maxLines: 1,
                    ),
                  ],
                ),
                Text(
                  date,
                  overflow: TextOverflow.ellipsis,
                  maxLines: 1,
                ),
              ]),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      Icon(
                        Icons.location_on_outlined,
                        color: Colors.blue[900],
                      ),
                      Text(
                        location,
                        overflow: TextOverflow.ellipsis,
                        maxLines: 1,
                      ),
                    ],
                  ),
                  Icon(
                    Icons.favorite_border,
                    color: Colors.blue[900],
                  )
                ],
              )
            ],
          ),
          leading: ClipRRect(
              borderRadius: BorderRadius.circular(10),
              child: Image.asset(
                'assets/image.png',
                height: 100,
                width: 100,
              )),
        )),

        //   Row(
        //     children: [

        //       Icon(icon, size: 100, color: Colors.blue[900]),
        //       SizedBox(
        //         width: 2,
        //       ),
        //       Flexible(
        // child: Column(
        //   crossAxisAlignment: CrossAxisAlignment.start,
        //           children: [
        //             Text(
        //               jobTitle,
        //               style:
        //                   TextStyle(fontSize: 19, fontWeight: FontWeight.bold),
        //               overflow: TextOverflow.ellipsis,
        //               maxLines: 1,
        //             ),
        //             Text(
        //               jobDescription,
        //               style:
        //                   TextStyle(fontSize: 15, fontWeight: FontWeight.w300),
        //               overflow: TextOverflow.ellipsis,
        //               maxLines: 1,
        //             ),

        //           ],
        //         ),
        //       )
        //     ],
        //   ),
        // ),
      ),
    );
  }
}
