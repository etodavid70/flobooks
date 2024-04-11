import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

void main() async {
  // Data to be sent to Django API
  var userData = {
   
    "password": "1234",

    "first_name": "etp",
    "last_name": "david",
    "email": "davideto18@gmail.com",
    "country": "Nigeria",
    "state": "lagos",
    "phoneNumber": "1234",
    "businessName": "hello world",
    "businessAddress": "hhi world",
    "present_package": "bronze",
  
  };

  // Encode the data as JSON
  var jsonBody = json.encode(userData);

  // Define the API endpoint
  var apiUrl = 'http://127.0.0.1:8000/signup/';

  try {
    // Make a POST request to the Django API
    var response = await http.post(
      Uri.parse(apiUrl),
      headers: {
        HttpHeaders.contentTypeHeader: 'application/json',
      },
      body: jsonBody,
    );

    // Check the response status code
    if (response.statusCode == 201|| response.statusCode==200) {
      print('Data sent successfully');
    } else {
      print('Failed to send data. Status code: ${response.statusCode}');
    }
  } catch (e) {
    print('Error: $e');
  }
}
