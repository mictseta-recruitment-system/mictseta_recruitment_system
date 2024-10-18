import 'package:flutter/material.dart';

class TextfieldPage extends StatelessWidget {
  final TextEditingController controller;
  final String hintText;
  final bool state;
  final IconData icon;

  final TextInputType keyBoardType;
  const TextfieldPage(
      {super.key,
      required this.controller,
      required this.hintText,
      required this.state,
      required this.icon,
      required this.keyBoardType});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          decoration: BoxDecoration(
            border: Border.all(
              color: Colors.blue,
              width: 2.0,
            ),
            borderRadius: BorderRadius.circular(10.0),
          ),
          child: TextField(
            keyboardType: keyBoardType,
            obscureText: state,
            controller: controller,
            decoration: InputDecoration(
              prefixIcon: Icon(
                icon,
                color: Colors.blue[900],
              ),
              hintText: hintText,
              border: InputBorder.none,
            ),
          ),
        ),
        SizedBox(height: 10)
      ],
    );
  }
}

class TextfieldPage2 extends StatelessWidget {
  final TextEditingController controller;
  final String hintText;
  final TextInputType keyBoardType;
  const TextfieldPage2({
    super.key,
    required this.controller,
    required this.hintText,
    required this.keyBoardType,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          decoration: BoxDecoration(
            border: Border.all(
              color: Colors.blue,
              width: 2.0,
            ),
            borderRadius: BorderRadius.circular(10.0),
          ),
          child: TextField(
            keyboardType: keyBoardType,
            controller: controller,
            decoration: InputDecoration(
              hintText: hintText,
              border: InputBorder.none,
              contentPadding: EdgeInsets.symmetric(horizontal: 20.0),
            ),
          ),
        ),
        SizedBox(
          height: 5,
        )
      ],
    );
  }
}

// class TextfieldPage3 extends StatefulWidget {
//   final TextEditingController controller;
//   final String hintText;
//   final TextInputType keyBoardType;
//   const TextfieldPage3({
//     Key? key,
//     required this.controller,
//     required this.hintText,
//     required this.keyBoardType,
//   });

//   @override
//   State<TextfieldPage3> createState() => _TextfieldPage3State();
// }

// class _TextfieldPage3State extends State<TextfieldPage3> {
//   bool _obscureText = true;
//   @override
//   Widget build(BuildContext context) {
//     return Column(
//       children: [
//         Container(
//           decoration: BoxDecoration(
//             border: Border.all(
//               color: Colors.blue,
//               width: 2.0,
//             ),
//             borderRadius: BorderRadius.circular(10.0),
//           ),
//           child: TextField(
//             controller: controller,
//             decoration: InputDecoration(
//                 border: OutlineInputBorder(
//                   borderSide:
//                       BorderSide(color: const Color.fromARGB(255, 14, 74, 163)),
//                   borderRadius: BorderRadius.circular(10),
//                 ),
//                 focusedBorder: OutlineInputBorder(
//                   borderSide:
//                       BorderSide(color: const Color.fromARGB(255, 15, 75, 165)),
//                   borderRadius: BorderRadius.circular(10),
//                 ),
//                 fillColor: Colors.blue[50],
//                 filled: true,
//                 suffixIcon: IconButton(
//                   icon: Icon(
//                     _obscureText ? Icons.visibility : Icons.visibility_off,
//                     color: Colors.blue[900],
//                   ),
//                   onPressed: () {
//                     setState(() {
//                       _obscureText = !_obscureText;
//                     });
//                   },
//                 ),
//                 prefixIcon: Icon(
//                   Icons.lock,
//                   color: Colors.blue,
//                 ),
//                 hintText: hintText),
//             obscureText: _obscureText,
//           ),
//         ),
//         SizedBox(
//           height: 5,
//         )
//       ],
//     );
//   }
// }

class TextFieldDetailsDisplay extends StatelessWidget {
  final String hintText;
  const TextFieldDetailsDisplay({super.key, required this.hintText});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          decoration: BoxDecoration(
            border: Border.all(
              color: Colors.blue,
              width: 1.0,
            ),
            borderRadius: BorderRadius.circular(5.0),
          ),
          child: TextField(
            decoration: InputDecoration(
              hintText: hintText,
              border: InputBorder.none,
              contentPadding: EdgeInsets.symmetric(horizontal: 20.0),
            ),
          ),
        ),
        SizedBox(
          height: 10,
        )
      ],
    );
  }
}
