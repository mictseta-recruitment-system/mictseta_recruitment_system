import 'package:flutter/material.dart';

class ExpansionTileChoose extends StatefulWidget {
  final String selectedValue;
  final List<String> valueS;
  const ExpansionTileChoose({
    super.key,
    required this.selectedValue,
    required this.valueS,
  });

  @override
  State<ExpansionTileChoose> createState() => _ExpansionTileChooseState();
}

class _ExpansionTileChooseState extends State<ExpansionTileChoose> {
  late String selectedValue;

  @override
  void initState() {
    super.initState();
    selectedValue = widget.selectedValue;
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          child: ExpansionTile(
            title: Text(selectedValue),
            children: widget.valueS.map((parValue) {
              return RadioListTile<String>(
                title: Text(parValue),
                value: parValue,
                groupValue: selectedValue,
                onChanged: (value) {
                  setState(() {
                    selectedValue = value!;
                  });
                },
              );
            }).toList(),
          ),
        ),
        SizedBox(height: 5),
      ],
    );
  }
}
