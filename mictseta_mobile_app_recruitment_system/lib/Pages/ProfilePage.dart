import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../Components/TextField.dart';


class Profilepage extends StatefulWidget {
  // final String? token;
  const Profilepage({super.key,   });

  @override
  State<Profilepage> createState() => _ProfilepageState();
}

class _ProfilepageState extends State<Profilepage> {
  
String token='';
final storage = FlutterSecureStorage();
@override
void initState() async{
  super.initState();
  token =await storage.read(key:'auth_token') as String;
}

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(10),
      child: Column(
        children: [
          GestureDetector(
            onTap: (){

            },
            child: Container(
              
              height: 200,
              width: 200,
              decoration: BoxDecoration(
                color: Colors.blue,
                borderRadius: BorderRadius.circular(100)),
              child: Icon(Icons.person,color: Colors.white,size:150),
            ),
          ),
          SizedBox(height: 10,),
          TextFieldDetailsDisplay(hintText: 'Name',),
          TextFieldDetailsDisplay(hintText: 'Surname',),
          TextFieldDetailsDisplay(hintText: 'Id Number',),
          TextFieldDetailsDisplay(hintText: 'Email',), ],
      ),
    );
  }
}
