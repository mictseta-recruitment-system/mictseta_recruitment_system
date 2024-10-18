import 'dart:convert';

import 'package:buttons_tabbar/buttons_tabbar.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_dropdown_search/flutter_dropdown_search.dart';
import 'package:flutter_intl_phone_field/flutter_intl_phone_field.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:form_builder_file_picker/form_builder_file_picker.dart';
import 'package:mictseta/Components/Buttons.dart';
import 'package:http/http.dart' as http;
import 'package:mictseta/Sign%20up%20files/Textfield.dart';
import 'package:text_field_validation/text_field_validation.dart';
import 'package:simple_month_year_picker/simple_month_year_picker.dart';

class ProfileInformation extends StatefulWidget {
  final Map<String, dynamic> userData;
  const ProfileInformation({super.key, required this.userData});

  @override
  State<ProfileInformation> createState() => _ProfileInformationState();
}

class _ProfileInformationState extends State<ProfileInformation> {
  String cellPhone = '';
  String? token;
  final storage = FlutterSecureStorage();
  final _formKey = GlobalKey<FormState>();

  @override
  void initState() {
    super.initState();
    _retrieveToken();
  }

  TextEditingController idNumberController = TextEditingController();
  TextEditingController phoneController = TextEditingController();
  TextEditingController nameController = TextEditingController();
  TextEditingController surnameController = TextEditingController();
  TextEditingController linkdenController = TextEditingController();
  TextEditingController personalWeblinkController = TextEditingController();
  TextEditingController disabilityController = TextEditingController();
  TextEditingController raceController = TextEditingController();
  TextEditingController _maritialStatusController = TextEditingController();
  TextEditingController qualificationController = TextEditingController();
  TextEditingController disabilityTypeController = TextEditingController();
  TextEditingController fieldController = TextEditingController();
  TextEditingController universityController = TextEditingController();
  String selectedDisabilityState = '';
  List<String> disabilityState = [
    'Yes',
    'No',
  ];
   String selectedStatus = '';
  List<String> qualificationStatus = [
    'In progess',
    'Completed',
  ];
  List<String> fieldOfStudy = [
    'Engineering',
    'Business',
    'administration',
    'Art',
    'Education',
    'Law',
    'Agriculture',
    'Business',
    'Health',
    'Humanities',
    'Anthropology',
    'Computers',
    'Language',
    'Mathematics',
    'Media',
    'Pharmacy',
    'Statistics',
  ];
  String selectedDisabilityType = '';
  List<String> disabilityType = [
    'Hearing loss',
    'Vision impairment',
    'Learning disabilities',
    'Autism',
    'Physical disability',
    'Intellectual disability',
    'Multiple disabilities',
    'Speech',
    'Cerebral palsy',
    'ADHD',
    'Traumatic brain injury',
    'Multiple sclerosis',
    'Blindness',
    'Epilepsy',
    'Mobility',
    'Concussion',
    'Impairment',
    'Medical',
    'Muscular dystrophy',
    'Neurological disorder',
    'Cognition',
    'Emotional disturbance',
    'Chronic condition',
    'Health impairments',
    'Other',
  ];

  String selectedRace = '';
  List<String> race = ['Black African', 'Coloured', 'White', 'Indian'];
  String selectedMaritialStatus = '';
  List<String> maritialStatus = [
    'Single',
    'Married',
    'Devorced',
    'Widowed',
  ];
  List<String> university = [
     
	'University of Cape Town'	,
	'University of the Witwatersrand',
	'Stellenbsoch University'	,
	'University of KwaZulu Natal'	,
	'University of Johannesburg'	,
	'University of Pretoria'	,
	'North-West University',
	'University of the Free State'	,
	'University of South Africa (UNISA)',	
	'University of the Western Cape'	,
	'Rhodes University	',
	'Durban University of Technology'	,
	'Tshwane University of Technology'	,
	'Nelson Mandela University'	,
	'University of Fort Hare'	,
	'Sefako Makgatho Health Sciences University'	,
	'University of Venda'	,
	'Cape Peninsula University of Technology'	,
	'University of Limpopo',
'Walter Sisulu University','University of Zululand',	'Vaal University of Technology'
  ];
  String selectedQualification = '';
  List<String> qualification = [
    "Bachelor's degree"
        "Diploma",
    "Master's Degree",
    "Certificate of Advanced Study",
    "Honours degree",
    "Doctoral degree",
    'Advanced Diploma',
    'National Diploma',
    'Higher National Certificate',
  ];

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

  String gender = '';
  Future<void> _updateProfile(
    String name,
    String surname,
    String idnumber,
    String cellphone,
    String personalWebsite,
    String linkedin,
  ) async {
    if (token == null) {
      print('Token is missing. Please log in.');
      return;
    } else if (idnumber.length != 13) {
      print('The ID number is invalid');
    }

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => Center(child: CircularProgressIndicator()),
    );

    var url = 'http://127.0.0.1:8000/rest_api/profile/';
    print('Here is token: $token');
// if(name.isNotEmpty&&surname.isNotEmpty&&idnumber)
    try {
      final response = await http.put(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Token $token',
        },
        body: jsonEncode({
          "name": name,
          "surname": surname,
          "phone": cellphone,
          "idnumber": idnumber,
          "linkedin_profile": linkedin,
          "personal_website": personalWebsite,
          "gender":
              int.parse(idnumber.substring(6, 9)) >= 5000 ? 'Male' : 'Female',
          "dob":int.parse(idnumber.substring(0, 5)),
          //0207235794089
        }),
      );
      Navigator.pop(context);

      if (response.statusCode == 201) {
        print('Profile updated successfully');
      } else if (response.statusCode == 302) {
      } else {
        print('Failed to update profile: ${response.body}');
      }
    } catch (e) {
      Navigator.pop(context);
      print('Error: $e');
    }
  }

  String id = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          centerTitle: true,
          title: Text('Edit Profile'),
          backgroundColor: Colors.blue[900],
          foregroundColor: Colors.white,
        ),
        body: DefaultTabController(
          length: 7,
          child: Padding(
            padding: const EdgeInsets.only(left: 10, right: 10, bottom: 20),
            child: Column(
              children: <Widget>[
                ButtonsTabBar(
                  backgroundColor: Colors.blue[600],
                  borderColor: Colors.blue,
                  unselectedBackgroundColor: Colors.white,
                  labelStyle: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                  unselectedLabelStyle: TextStyle(
                    color: Colors.blue[600],
                    fontWeight: FontWeight.bold,
                  ),
                  borderWidth: 2,
                  unselectedBorderColor: Colors.blue,
                  radius: 30,
                  tabs: [
                    Tab(
                      icon: Icon(Icons.person),
                      text: "Personal information",
                    ),
                    Tab(
                      icon: Icon(Icons.school_outlined),
                      text: "Academic Qualification",
                    ),
                    Tab(
                      icon: Icon(Icons.file_copy_rounded),
                      text: "Computer and soft skills",
                    ),
                    Tab(
                      icon: Icon(Icons.record_voice_over_outlined),
                      text: "Languages",
                    ),
                    Tab(
                      icon: Icon(Icons.wallet_travel_rounded),
                      text: "Work Experience",
                    ),
                    Tab(
                      icon: Icon(Icons.room_preferences_outlined),
                      text: "References",
                    ),
                    Tab(
                      icon: Icon(Icons.file_copy_rounded),
                      text: "Supporting Documents",
                    ),
                  ],
                ),
                Form(
                  child: Expanded(
                    child: TabBarView(
                      children: [

                        Form(
                          autovalidateMode: AutovalidateMode.onUserInteraction,
                          key: _formKey,
                          child: SingleChildScrollView(
                            child: Column(
                              children: [
                                AuthTextField(
                                  keyBoardType: TextInputType.number,
                                  icon: Icons.numbers,
                                  placeholder: widget.userData['idnumber'] == ''
                                      ? 'ID Number'
                                      : widget.userData['idnumber'] ?? 'NaN',
                                  controller: idNumberController,
                                  onValidate: (value) =>
                                      TextFieldValidation.name(value!),
                                ),
                                AuthTextField(
                                  keyBoardType: TextInputType.name,
                                  icon: Icons.person_2_outlined,
                                  placeholder: widget.userData['name'] == ''
                                      ? 'Name'
                                      : widget.userData['name'] ?? 'NaN',
                                  controller: nameController,
                                  onValidate: (value) =>
                                      TextFieldValidation.name(value!),
                                ),
                                AuthTextField(
                                  keyBoardType: TextInputType.name,
                                  icon: Icons.person_2_outlined,
                                  placeholder: widget.userData['surname'] == ''
                                      ? 'Surname '
                                      : widget.userData['surname'] ?? 'NaN',
                                  controller: surnameController,
                                  onValidate: (value) =>
                                      TextFieldValidation.name(value!),
                                ),
                                IntlPhoneField(
                                  languageCode: 'ZA',
                                  controller: phoneController,
                                  decoration: InputDecoration(
                                    labelText: widget.userData['phone'] == ''
                                        ? 'Cellphone number'
                                        : widget.userData['phone'] ?? 'NaN',
                                    border: OutlineInputBorder(
                                      borderSide: BorderSide(),
                                    ),
                                  ),
                                  initialCountryCode: 'ZA',
                                  onChanged: (phone) {
                                    setState(() {
                                      cellPhone = phone.completeNumber;
                                    });
                                  },
                                ),
                                AuthTextField(
                                  keyBoardType: TextInputType.url,
                                  icon: Icons.add_link_outlined,
                                  placeholder: widget
                                              .userData['linkedin_profile'] ==
                                          ''
                                      ? 'Your linkedin'
                                      : widget.userData['linkedin_profile'] ??
                                          'NaN',
                                  controller: linkdenController,
                                  onValidate: (value) =>
                                      TextFieldValidation.linkedin(value!),
                                ),
                                AuthTextField(
                                  keyBoardType: TextInputType.url,
                                  icon: Icons.add_link_outlined,
                                  placeholder: widget
                                              .userData['personal_website'] ==
                                          ''
                                      ? 'Your Personal website'
                                      : widget.userData['linkedin_profile'] ??
                                          'NaN',
                                  controller: personalWeblinkController,
                                  onValidate: (value) =>
                                      TextFieldValidation.url(value!),
                                ),
                                SizedBox(height: 10),
                                FlutterDropdownSearch(
                                  textController: _maritialStatusController,
                                  items: maritialStatus,
                                  
                                ),
                                SizedBox(height: 10),
                                FlutterDropdownSearch(
                                  textController: raceController,
                                  items: race,
                                  
                                ),
                                SizedBox(height: 10),
                                ExpansionTile(
                                  title: Text('Disability'),
                                  children: disabilityState.map((state) {
                                    return RadioListTile<String>(
                                      title: Text(state),
                                      value: state,
                                      groupValue: selectedDisabilityState,
                                      onChanged: (value) {
                                        setState(() {
                                          selectedDisabilityState = value!;
                                        });
                                      },
                                    );
                                  }).toList(),
                                ),
                                if (selectedDisabilityState == 'Yes')
                                  FlutterDropdownSearch(
                                    textController: disabilityTypeController,
                                    items: disabilityType, 
                                  ),
                                if (selectedDisabilityState == 'Other')
                                  AuthTextField(
                                    keyBoardType: TextInputType.name,
                                    icon: Icons.person_2_outlined,
                                    placeholder: 'Disability Name',
                                    controller: disabilityController,
                                    onValidate: (value) =>
                                        TextFieldValidation.name(value!),
                                  ),
                                SizedBox(height: 20),
                              ],
                            ),
                          ),
                        ),
//============================= Academic Qualification =============================================================================
                        Column(
                          children: [
                            FlutterDropdownSearch(
                              textController: qualificationController,
                              items: qualification,
                              
                            ),
                            SizedBox(height: 10),
                            FlutterDropdownSearch(
                              textController: fieldController,
                              items: fieldOfStudy,
                              
                            ),
                            SizedBox(height: 10),
                            FlutterDropdownSearch(
                              textController: universityController,
                              items: university,
                              
                            ),
                            SizedBox(height: 10),
                            FlutterDropdownSearch(
                              textController: universityController,
                              items: university,
                              
                            ),
                            SizedBox(height: 10),
                            ExpansionTile(
                                  title: Text('Qualification Status'),
                                  children: qualificationStatus.map((status) {
                                    return RadioListTile<String>(
                                      title: Text(status),
                                      value: status,
                                      groupValue: selectedStatus,
                                      onChanged: (value) {
                                        setState(() {
                                          selectedStatus = value!;
                                        });
                                      },
                                    );
                                  }).toList(),
                                ),
                            SizedBox(height: 10),
                            ElevatedButton(
              onPressed: () async { 
                final selectedDate =
                    await SimpleMonthYearPicker.showMonthYearPickerDialog(
                        context: context,
                        titleTextStyle: TextStyle(),
                        monthTextStyle: TextStyle(),
                        yearTextStyle: TextStyle(),
                        disableFuture:false
                         );  
                print('Selected date: $selectedDate');
              },
              child: const Text('show dialog'),
            ),
                            SizedBox(height: 10),
                             FormBuilderFilePicker(
                              name: "attachments",
                              previewImages: false,
                              allowMultiple: true,
                              withData: true,
                              typeSelectors: [
                                TypeSelector(
                                  type: FileType.any,
                                  selector: Row(
                                    children: <Widget>[
                                      Icon(Icons.add_circle),
                                      Padding(
                                        padding:
                                            const EdgeInsets.only(left: 8.0),
                                        child: Text("Add documents"),
                                      ),
                                    ],
                                  ),
                                ),
                                if (!kIsWeb)
                                  TypeSelector(
                                    type: FileType.any,
                                    selector: Row(
                                      children: <Widget>[
                                        Icon(Icons.add_photo_alternate),
                                        Padding(
                                          padding:
                                              const EdgeInsets.only(left: 8.0),
                                          child: Text("Add Transcript"),
                                        ),
                                      ],
                                    ),
                                  ),
                              ],
                            ),
                            SizedBox(height: 10),
                          ],
                        ),
//======================= Computer SKills ===================================
                        Column(
                          children: [
                            OutlinedButton(
                                onPressed: () {}, child: Text('Update')),
                          ],
                        ),
//======================= Languages ===================================

                        Column(
                          children: [
                            OutlinedButton(
                                onPressed: () {}, child: Text('Update')),
                          ],
                        ),
//======================= Work Experience ===================================

                        Column(
                          children: [
                            OutlinedButton(
                                onPressed: () {}, child: Text('Update')),
                          ],
                        ),
//======================= Languages ===================================

                        Column(
                          children: [
                            OutlinedButton(
                                onPressed: () {}, child: Text('Update')),
                          ],
                        ),
//======================= Supporting Information ===================================

                        Column(
                          children: [
                            Center(child: Text('Supporting Information')),
                            FormBuilderFilePicker(
                              name: "attachments",
                              previewImages: false,
                              allowMultiple: true,
                              withData: true,
                              typeSelectors: [
                                TypeSelector(
                                  type: FileType.any,
                                  selector: Row(
                                    children: <Widget>[
                                      Icon(Icons.add_circle),
                                      Padding(
                                        padding:
                                            const EdgeInsets.only(left: 8.0),
                                        child: Text("Add documents"),
                                      ),
                                    ],
                                  ),
                                ),
                                if (!kIsWeb)
                                  TypeSelector(
                                    type: FileType.image,
                                    selector: Row(
                                      children: <Widget>[
                                        Icon(Icons.add_photo_alternate),
                                        Padding(
                                          padding:
                                              const EdgeInsets.only(left: 8.0),
                                          child: Text("Add images"),
                                        ),
                                      ],
                                    ),
                                  ),
                              ],
                            ),
                            OutlinedButton(
                                onPressed: () {}, child: Text('Update')),

                            //                 DateTimeFormField(
                            //   decoration: const InputDecoration(
                            //     labelText: 'Enter Date',
                            //   ),
                            //   firstDate: DateTime.now().add(const Duration(days: 10)),
                            //   lastDate: DateTime.now().add(const Duration(days: 40)),
                            //   initialPickerDateTime: DateTime.now().add(const Duration(days: 20)),
                            //   onChanged: (DateTime? value) {
                            //     selectedDate = value;
                            //   },
                            // ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
                Buttons(
                    child: 'Update',
                    backgroundColor: Colors.blue,
                    foregroundColor: Colors.white,
                    onTap: () {
                      _updateProfile(
                        nameController.text,
                        surnameController.text,
                        idNumberController.text,
                        cellPhone,
                        personalWeblinkController.text,
                        linkdenController.text,
                      );
                    })
              ],
            ),
          ),
        ));
  }
}
