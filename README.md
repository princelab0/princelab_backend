# princelab_backend
## User CRUD operation API

1. /api/user/
Above api contain GET,POST,PUT,PATCH,DELETE methos 
-GET method return all the user
<img width="860" alt="image" src="https://github.com/princelab0/princelab_backend/assets/112973122/6d0bc159-080f-4cae-9cb4-2b9621bb4c57">

-POST method with data (email, password) register the user with respod return email of user
Note:- with fake eamil you can register a user but not able to login because after login activation link will be send to user email to activate user
<img width="862" alt="image" src="https://github.com/princelab0/princelab_backend/assets/112973122/0dfd3e19-951d-42a0-acb2-d1e15bc4c352">

Likewise you can used PUT,PATCH, DELETE

2. /api/login
   Above api contain POST method with data (email, oassword) return user info and token
   <img width="868" alt="image" src="https://github.com/princelab0/princelab_backend/assets/112973122/a235d008-70a8-4b42-8f8f-2d2d4310739e">

3. api/change_password/
   Above API contain POST methos to change user password with data(email,current_password,new_password) and a respond with "Password Change"
   <img width="860" alt="image" src="https://github.com/princelab0/princelab_backend/assets/112973122/25e66037-fbd0-438f-b99f-ad6089fac017">

4. api/forgot_password_otp_send/
   Above API contain POST method to send OTP(4 digits) to user email for forgot password need data(email) and respond with "OTP has been send to your email."
   Note:- OTP expire in 2 minute
   ![image](https://github.com/princelab0/princelab_backend/assets/112973122/3398acd4-8a7a-4bcf-93b8-dca09cd8c20c)
5. api/forgot_password_otp_validare_change_password/
   Above API contain POST method to reset the password after OTP has been send with data (email,otp,new_password) wit respond "Password reset successfully"
   ![image](https://github.com/princelab0/princelab_backend/assets/112973122/905f667c-cd51-44b8-9b7a-93b4d6be38a3)

## Service API
6. api/service/
   Above API contain GET operation with data (token of customer) and parameter in not mandatory
   <img width="866" alt="image" src="https://github.com/princelab0/princelab_backend/assets/112973122/a4329306-cb91-4097-83a1-75b6650223dd">



   

