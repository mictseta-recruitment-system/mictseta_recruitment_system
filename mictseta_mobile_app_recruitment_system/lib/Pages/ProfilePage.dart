import 'package:flutter/material.dart';

import '../Components/TextField.dart';


class Profilepage extends StatelessWidget {
  const Profilepage({super.key});

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
