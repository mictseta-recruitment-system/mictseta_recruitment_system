// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import 'MICSETAFeedback.dart';

class Notificationpage extends StatefulWidget {
  // final String? token;
  const Notificationpage({super.key, });

  @override
  State<Notificationpage> createState() => _NotificationpageState();
}

class _NotificationpageState extends State<Notificationpage> {
  
 String? token;  
  final storage = FlutterSecureStorage();

  @override
  void initState() {
    super.initState();
    _retrieveToken();
  }

  Future<void> _retrieveToken() async {
    String? tkn = await storage.read(key: 'auth_token');
    if (tkn != null) {
      setState(() {
        token = tkn;
      });
    } else {
      print('No token found');
    }
  }

  
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
  //           CupertinoLeftScroll(
  //   // important, each Row must have different key.
  //   // DO NOT use '$index' as Key! Use id or title.
  //   key: Key('TODO: your key'),
  //   // left scroll widget will auto close while the other widget is opened and has same closeTag.
  //   // 当另一个有相同closeTag的组件打开时，其他有着相同closeTag的组件会自动关闭.
  //   closeTag: LeftScrollCloseTag('TODO: your tag'),
  //   buttonWidth: 80,
  //   child: Container(
  //     height: 60,
  //     color: Colors.white,
  //     alignment: Alignment.center,
  //     child: Text('👈 Try Scroll Left'),
  //   ),
  //   buttons: <Widget>[
  //     LeftScrollItem(
  //       text: 'edit',
  //       color: Colors.orange,
  //       onTap: () {
  //         print('edit');
  //       },
  //     ),
  //     LeftScrollItem(
  //       text: 'delete',
  //       color: Colors.red,
  //       onTap: () {
  //         print('delete');
  //       },
  //     ),
  //   ],
  //   onTap: () {
  //     print('tap row');
  //   },
  // ) 
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
 