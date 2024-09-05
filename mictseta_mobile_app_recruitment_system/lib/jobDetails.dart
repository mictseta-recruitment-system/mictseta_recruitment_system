import 'package:flutter/material.dart';

class JobdetailsPage extends StatefulWidget {
  const JobdetailsPage({super.key});

  @override
  State<JobdetailsPage> createState() => _JobdetailsPageState();
}

class _JobdetailsPageState extends State<JobdetailsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor:Colors.blue[100],
      appBar:AppBar(
        title:Text('Job Title'),
        centerTitle: true,
        foregroundColor: Colors.white,
        backgroundColor: Colors.blue[900],
      ),
      body:Padding(
        padding: const EdgeInsets.all(8.0),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children:[
            Center(child: Image.asset('assets/image.png',height: 200,width:200,fit:BoxFit.cover)),
            SizedBox(height:10),
            Text('Description:',style:TextStyle(fontWeight: FontWeight.bold,fontSize: 20))
          , SizedBox(height:5),
            Text('The Job needs someone with commitment and able to work under pressure and also work with white people',style:TextStyle(fontWeight: FontWeight.w300)),
            SizedBox(height:5),
            Text('Requirements:',style:TextStyle(fontWeight: FontWeight.bold,fontSize: 20))
          , SizedBox(height:5),
           Text('- Java\n- JavaScripts\n- Python\n- Ruby\n- HTML\n- PhP\n- CSS'),
           SizedBox(height:10),
           
           OutlinedButton(
                  onPressed: () {},
                  style: ButtonStyle(
                    minimumSize: WidgetStatePropertyAll(
                      Size(double.infinity, 55),
                    ),
                    foregroundColor: WidgetStatePropertyAll(Colors.blue[50]),
                    backgroundColor: WidgetStatePropertyAll(Colors.blue),
                    shape: WidgetStatePropertyAll(RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(5))),
                    side: WidgetStateProperty.resolveWith<BorderSide>(
                      (Set<WidgetState> states) {
                        return BorderSide(
                          color: const Color.fromARGB(255, 14, 74, 165),
                          width: 1.0,
                        );
                      },
                    ),
                  ),
                  child: Text(
                    'Apply now',
                  ),
                ),
          
          
          ]),
        ),
      )
    );
  }
}