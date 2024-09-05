// ignore_for_file: prefer_const_literals_to_create_immutables, prefer_const_constructors

import 'package:flutter/material.dart';

import 'Components/informationData.dart';

class MoreInformationPage extends StatefulWidget {
  final String tabName;
  const MoreInformationPage({super.key, required this.tabName});

  @override
  State<MoreInformationPage> createState() => _MoreInformationPageState();
}

class _MoreInformationPageState extends State<MoreInformationPage> {
  TextEditingController helpController = TextEditingController();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blue[100],
      appBar: AppBar(
        title: Text(widget.tabName),
        backgroundColor: Colors.blue[900],
        foregroundColor: Colors.white,
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(10.0),
        child: SingleChildScrollView(
          child: Column(
            children: [
              if (widget.tabName == 'About Us')
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Informationdata(
                        title: 'Our Vision',
                        description: 'Cutting edge future skills'),
                    Informationdata(
                        title: 'Our Mission',
                        description:
                            'To strategically lead the MICT sector skills development system in support of meaningful economic participation of our beneficiaries, for improved socio-economic conditions.'),
                    Informationdata(
                        title: 'Our Values',
                        description:
                            'Customer Centricity\nEthical\nInnovative\nCommitted\nMeritocracy\nCollaborative'),
                    Informationdata(
                        title: 'Our Mandate',
                        description:
                            'The Media, Information and Communication Technologies Sector Education and Training Authority (MICT SETA) is a public entity established in terms of the Skills Development Act, 1998 (Act No. 97 of 1998). The MICT SETA plays a pivotal role in achieving South Africa’s skills development and economic growth within the sub-sectors it operates namely; Advertising, Film and Electronic Media, Electronics, Information Technology and Telecommunications.'),
                  ],
                ),
              if (widget.tabName == 'Contact Us')
                Column(
                  children: [
                    Informationdata(
                        title: 'This  Vision',
                        description: 'Cutting edge future skills'),
                  ],
                ),
              if (widget.tabName == 'Help Center')
                Column(
                  children: [
                    
                    Text(
                      "Please let us know any issue that you're encountering using the App so to get you issue resolved",
                      style: TextStyle(
                          fontWeight: FontWeight.w500, color: Colors.grey),
                    ),
                    SizedBox(height:10),
                    Container(
                      decoration: BoxDecoration(
                        border: Border.all(
                          color: Colors.blue,
                          width: 1.0,
                        ),
                        borderRadius: BorderRadius.circular(5.0),
                      ),
                      child: TextField(
                        controller: helpController,
                        maxLines: 10,
                        decoration: InputDecoration(
                          labelText: "Your Issue?",
                          border: InputBorder.none,
                          contentPadding:
                              EdgeInsets.symmetric(horizontal: 20.0),
                        ),
                      ),
                    ),
                    SizedBox(
                      height: 10,
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.end,
                      children: [
                        Text('Send',style:TextStyle(fontSize:20)),
                        IconButton(
                            onPressed: () {},
                            icon: Icon(
                              Icons.send_outlined,
                              color: Colors.blue,
                              size: 20,
                            ))
                      ],
                    )
                  ],
                ),
            ],
          ),
        ),
      ),
    );
  }
}
