import 'package:flutter/material.dart';
import 'package:mictseta_mobile_app_recruitment_system/Components/Buttons.dart';

class JobdetailsPage extends StatefulWidget {
  final  dynamic jobDetails;
  const JobdetailsPage({super.key, required this.jobDetails});

  @override
  State<JobdetailsPage> createState() => _JobdetailsPageState();
}

class _JobdetailsPageState extends State<JobdetailsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: Colors.blue[100],
        appBar: AppBar(
          title: Text('Job Title'),
          centerTitle: true,
          foregroundColor: Colors.white,
          backgroundColor: Colors.blue[900],
        ),
        body: Padding(
          padding: const EdgeInsets.all(8.0),
          child: SingleChildScrollView(
            child:
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Center(
                  child: Image.asset('assets/image.png',
                      height: 200, width: 200, fit: BoxFit.cover)),
              SizedBox(height: 10),
               Text('Title',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20)),
              Text(widget.jobDetails['title'],
                  
                  style: TextStyle(fontWeight: FontWeight.w300)),
              SizedBox(height: 5),
              Text('Description:',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20)),
              SizedBox(height: 5),
              Text(widget.jobDetails['description'],
                  
                  style: TextStyle(fontWeight: FontWeight.w300)),
              SizedBox(height: 5),
              Text('Requirements:',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20)),
              SizedBox(height: 5),
              Text(
                  '- Java\n- JavaScripts\n- Python\n- Ruby\n- HTML\n- PhP\n- CSS'),
              SizedBox(height: 10),
              Buttons(onTap: () {  },
              backgroundColor: Colors.white,
              foregroundColor: const Color.fromARGB(255, 13, 74, 167),
              child: 'Apply Now',)
            ]),
          ),
        ));
  }
}
