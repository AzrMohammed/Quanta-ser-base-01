
// window.onload = function() {
//  alert("let's go!");
// }

function myFunction() {
  var x = document.getElementById("phonea").value;
  alert(x);
  // document.getElementById("demo").innerHTML = "You wrote: " + x;
}

function select_product_item(name)
{
  alert("cameccc");
  alert("cameccc=="+name);
  $('#product_sugg').val(name)
}

function get_product_list_suggestion()
{


    var csrftoken = getCookie('csrftoken');

    phone_val = $('#product_sugg').val()
    var url = $('#url_product_list_suggestion').val()
    // el_list = document.getElementById("product_li")

    document.getElementById("product_li").innerHTML = "";

    alert(phone_val)
        $.ajax({
               type: "POST",
               url: url,
               headers: {"X-CSRFToken": csrftoken},
               data: {"phone":"ca"}, // serializes the form's elements.
               success: function(data)
               {

                 alert(JSON.stringify(data))

                 product_list = data.RESPONSE_DATA.product_list

                 for (i = 0; i < product_list.length; i++) {
                   each_pro =  product_list[i]
                   document.getElementById("product_li").innerHTML =document.getElementById("product_li").innerHTML  + '<a onclick="select_product_item(\''+each_pro.name+'\')" class="dropdown-item">'+each_pro.name+ '</a>';
                   // alert(each_pro.name)
                   // x += myObj.cars[i];
                }




                 // var leng =
                 // for()


                 // <a class="dropdown-item"> Apple Watch - <br> Price: Rs. 3,000 [Stock in Hand: 34 ] </a>

                 // <a class="dropdown-item"> Apple Watch - <br> Price: Rs. 3,000 [Stock in Hand: 34 ] </a>
                 // user_list = data.RESPONSE_DATA.user_data
                 // alert(JSON.stringify(user_list))
                 // JSON.parse
                // processResponse(data)

               }
             });
}

function get_user_suggestion()
{

    var csrftoken = getCookie('csrftoken');

    phone_val = $('#phone_primary').val()

    if(phone_val.length > 9)
    {


    var url = $('#url_user_suggestion').val()
    alert(phone_val)
        $.ajax({
               type: "POST",
               url: url,
               headers: {"X-CSRFToken": csrftoken},
               data: {"phone":phone_val}, // serializes the form's elements.
               success: function(data)
               {

                 // alert(JSON.stringify(data))
                 user_data = data.RESPONSE_DATA.user_data

                 alert(JSON.stringify(user_data.first_name))
                 // $("#username"+id_suffix).val(data_usermeta.fields.username)
                 $("#username").val(user_data.first_name)
                 // $("#email"+id_suffix).val(data_usermeta.fields.email)
                 //
                 // $("#phone_primary"+id_suffix).val(data_user_profile.fields.phone_primary)
                 //
                 $("#location_area").val(user_data.location_area)
                 $("#location_sublocality").val(user_data.location_sublocality)
                 $("#location_locality").val(user_data.location_locality)
                 $("#location_city").val(user_data.location_city)
                 $("#location_pincode").val(user_data.location_pincode)

                 // JSON.parse
                // processResponse(data)

               }
             });
           }
}

function loginCheck (is_loggedin)
{

  alert("Cakked== "+ is_loggedin);
// let d = new Date();
//    alert("Today's date is " + d);
  if(is_loggedin == 'True')
   {
     // print('sdss')
   }
  else
  {
     // alert("aaB");
     // window.location.replace($('#login_url').val());

  }


}



function EnableProduct(product_id)
{


    var csrftoken = getCookie('csrftoken');

    var url = $('#ul_user_status').val()

        $.ajax({
               type: "POST",
               url: url,
               headers: {"X-CSRFToken": csrftoken},
               data: {"product_id":""+product_id, "status":"ENABLE"}, // serializes the form's elements.
               success: function(data)
               {
                 // alert(JSON.stringify(data))
                // processResponse(data)

               }
             });


}


function DisableProduct(product_id)
{


  var csrftoken = getCookie('csrftoken');


  var url = $('#ul_user_status').val()

      $.ajax({
             type: "POST",
             url: url,
             headers: {"X-CSRFToken": csrftoken},
             data: {"product_id":""+product_id, "status":"DISABLE"}, // serializes the form's elements.
             success: function(data)
             {
               // alert(JSON.stringify(data))
              // processResponse(data)

             }
           });


}


function deActivateUser(username)
{

var csrftoken = getCookie('csrftoken');

var url = $('#ul_user_status').val()

    $.ajax({
           type: "POST",
           url: url,
           headers: {"X-CSRFToken": csrftoken},
           data: {"product_id":product_id, "status":"DISABLE"}, // serializes the form's elements.
           success: function(data)
           {
             // alert(JSON.stringify(data))
            // processResponse(data)

           }
         });

}


function activateUser(username)
{


  var csrftoken = getCookie('csrftoken');

  var url = $('#ul_user_status').val()

      $.ajax({
             type: "POST",
             url: url,
             headers: {"X-CSRFToken": csrftoken},
             data: {"username":username, "user_status":"UE"}, // serializes the form's elements.
             success: function(data)
             {
               // alert(JSON.stringify(data))
              // processResponse(data)

             }
           });


}

function proceedUserLogin()
{

  $('#error_el').text("");
  var form = $('#login_form');

  var formData = $(form).serialize();
  var url = form.attr('action');

      var username_v = $('#username').val();

      var password_v = $('#password').val()

      if(username_v == null || username_v === "")
      {
        $('#error_el').text("User Name not valid");
      }
      else if(password_v == null || password_v === "")
      {
        $('#error_el').text("Password not valid");
      }
      else
      $.ajax({
             type: "POST",
             url: url,
             data: form.serialize(), // serializes the form's elements.
             success: function(data)
             {
                 // alert(JSON.stringify(data)); // show response from the php script.

                 if(data.SUCCESS)
                  {
                    window.location.replace($('#login_success').val());
                    // alert(JSON.stringify(data))
                    // alert("successz"+data.RESPONSE_MESSAGE)

                  }
                 else
                 {
                   $('#error_el').text("Invalid Credentials");
                   // alert(JSON.stringify(data.ERRORS))
                 }

             }
           });
}

function proceedEdit(username)
{

is_edit = true;



var csrftoken = getCookie('csrftoken');
$.ajax({
      type: "POST",
      url: $("#da_fetch").val(),
      headers: {"X-CSRFToken": csrftoken},
      // url: "/get_da_details/",
      data: {username:username}, // serializes the form's elements.
      success: function(data)
      {
        $('#registerBoy').modal('toggle');
          // alert(JSON.stringify(data)); // show response from the php script.
          if(data.SUCCESS)
           {

             // alert(JSON.stringify(data))

             data_usermeta = JSON.parse(data.user_meta)[0]
             data_user_profile = JSON.parse(data.user_profile)[0]
             data_da_profile = JSON.parse(data.da_profile)[0]

             id_suffix = "";
             if(!(is_edit))
             id_suffix = "_v";
             // data_usermeta = data_json[0]
             // alert(JSON.stringify(data_usermeta))

             $("#pk"+id_suffix).val(data_usermeta.pk)
             if(($('input#header_type').val()) == "1"){
               $("#exampleModalLabel").text("Update Customer Care Boy")
               $("#btn_add_agent").html("UPDATE AGENT")
               console.log("kdsdsdsals");

             }else {
               $("#exampleModalLabel").text("Update a Delivery Boy")
               $("#btn_add_agent").html("UPDATE AGENT")
               console.log("kdsdsdssdsdsals");

             }

             console.log("ksals");


             $("#username"+id_suffix).val(data_usermeta.fields.username)
             $("#first_name"+id_suffix).val(data_usermeta.fields.first_name)
             $("#email"+id_suffix).val(data_usermeta.fields.email)

             $("#phone_primary"+id_suffix).val(data_user_profile.fields.phone_primary)
             $("#phone_secondary"+id_suffix).val(data_user_profile.fields.phone_secondary)
             $("#location_area"+id_suffix).val(data_user_profile.fields.location_area)
             $("#location_sublocality"+id_suffix).val(data_user_profile.fields.location_sublocality)
             $("#location_locality"+id_suffix).val(data_user_profile.fields.location_locality)
             $("#location_city"+id_suffix).val(data_user_profile.fields.location_city)
             $("#location_pincode"+id_suffix).val(data_user_profile.fields.location_pincode)


             // $("#profile_pic_v").src(data_user_profile.fields.profile_pic)
             var server_prefix = $("#pic_server_prefix").val();
             // alert(server_prefix+data_user_profile.fields.profile_pic);


             var state_key = data_user_profile.fields.location_state;
             var state_key_val = "";

             var mapped_state = $('#location_state option').map(function() {
             var obj_state = {};
             obj_state[this.value] = this.textContent;
             if(state_key == this.value)
               state_key_val = this.textContent;
             return obj_state;
           });

// http://127.0.0.1:8000/media/

             $("#location_state"+id_suffix).val(state_key)


             $("#profile_pic_v"+id_suffix).attr("src",  server_prefix+data_user_profile.fields.profile_pic);
             $("#driving_liscence_pic_v"+id_suffix).attr("src",  server_prefix+data_da_profile.fields.driving_liscence_pic);
             $("#pan_card_pic_v"+id_suffix).attr("src", server_prefix+data_da_profile.fields.pan_card_pic);
             $("#rc_pic_v"+id_suffix).attr("src", server_prefix+data_da_profile.fields.rc_pic);


             // $("#username_v").val(JSON.stringify(data))

           }
          else
          {
            alert(JSON.stringify(data.ERRORS))
          }

      }
    });


}

function proceedView(username)
{
  is_edit = false;



var csrftoken = getCookie('csrftoken');
$.ajax({
      type: "POST",
      url: $("#da_fetch").val(),
      headers: {"X-CSRFToken": csrftoken},
      // url: "/get_da_details/",
      data: {username:username}, // serializes the form's elements.
      success: function(data)
      {
        $('#registerBoyView').modal('toggle');
          // alert(JSON.stringify(data)); // show response from the php script.
          if(data.SUCCESS)
           {

             // alert(JSON.stringify(data))

             data_usermeta = JSON.parse(data.user_meta)[0]
             data_user_profile = JSON.parse(data.user_profile)[0]
             data_da_profile = JSON.parse(data.da_profile)[0]

             id_suffix = "";
             if(!(is_edit))
             id_suffix = "_v";
             // data_usermeta = data_json[0]
             // alert(JSON.stringify(data_usermeta))

             $("#pk"+id_suffix).val(data_usermeta.pk)
             $("#username"+id_suffix).text(data_usermeta.fields.username)
             $("#first_name"+id_suffix).text(data_usermeta.fields.first_name)
             $("#email"+id_suffix).text(data_usermeta.fields.email)

             $("#phone_primary"+id_suffix).text(data_user_profile.fields.phone_primary)
             $("#phone_secondary"+id_suffix).text(data_user_profile.fields.phone_secondary)
             $("#location_area"+id_suffix).text(data_user_profile.fields.location_area)
             $("#location_sublocality"+id_suffix).text(data_user_profile.fields.location_sublocality)
             $("#location_locality"+id_suffix).text(data_user_profile.fields.location_locality)
             $("#location_city"+id_suffix).text(data_user_profile.fields.location_city)
             $("#location_pincode"+id_suffix).text(data_user_profile.fields.location_pincode)


             // $("#profile_pic_v").src(data_user_profile.fields.profile_pic)
             var server_prefix = $("#pic_server_prefix").val();
             // alert(server_prefix+data_user_profile.fields.profile_pic);


             var state_key = data_user_profile.fields.location_state;
             var state_key_val = "";

             var mapped_state = $('#location_state option').map(function() {
             var obj_state = {};
             obj_state[this.value] = this.textContent;
             if(state_key == this.value)
               state_key_val = this.textContent;
             return obj_state;
           });


// http://127.0.0.1:8000/media/

             $("#location_state"+id_suffix).val(state_key_val)


             $("#profile_pic_v"+id_suffix).attr("src",  server_prefix+data_user_profile.fields.profile_pic);
             $("#driving_liscence_pic_v"+id_suffix).attr("src",  server_prefix+data_da_profile.fields.driving_liscence_pic);
             $("#pan_card_pic_v"+id_suffix).attr("src", server_prefix+data_da_profile.fields.pan_card_pic);
             $("#rc_pic_v"+id_suffix).attr("src", server_prefix+data_da_profile.fields.rc_pic);


             // $("#username_v").val(JSON.stringify(data))

           }
          else
          {
            // alert(JSON.stringify(data.ERRORS))
          }

      }
    });

}





function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function registerCustomerCare() {
var form = $('#register_customer_care_form');

var formData = $(form).serialize();
var url = form.attr('action');

 $('#error_el').val("")
 $('#success_el').val("")

    $.ajax({
           type: "POST",
           url: url,
           enctype:"multipart/form-data",
           data: new FormData(document.getElementById("register_customer_care_form")), // serializes the form's elements.
           processData: false,
           contentType: false,
           success: function(data)
           {
               // alert(JSON.stringify(data)); // show response from the php script.
               processResponse(data)

           }
         });

}

function registerAgent() {
var form = $('#register_agent_form');

var formData = $(form).serialize();
var url = form.attr('action');

 $('#error_el').val("")
 $('#success_el').val("")

    $.ajax({
           type: "POST",
           url: url,
           enctype:"multipart/form-data",
           data: new FormData(document.getElementById("register_agent_form")), // serializes the form's elements.
           processData: false,
           contentType: false,
           success: function(data)
           {
               // alert(JSON.stringify(data)); // show response from the php script.
               processResponse(data)

           }
         });

}






function processResponse(data)
{
  if(data.SUCCESS)
   {
     // alert(JSON.stringify(data))
   $('#success_el').text(data.RESPONSE_MESSAGE)

   $('#register_agent_form').trigger("reset");
   $('#create_order_form_parent').trigger("reset");

   window.setTimeout( location.reload(), 4000 );
   }
  else
  {


    // alert(JSON.stringify(data.ERRORS))
    $('#error_el').text(data.ERRORS)

  }
}

function createOrder()
{
  var form = $('#create_order_form');

  var formData = $(form).serialize();
  var url = form.attr('action');
  // alert(JSON.stringify(formData));

      $.ajax({
             type: "POST",
             url: url,
             data: form.serialize(), // serializes the form's elements.
             success: function(data)
             {
               alert(JSON.stringify(data))
               $('#create_order_form').trigger("reset");
               window.setTimeout( location.reload(), 4000 );
              // processResponse(data)

             }
           });

}


function openDaRegisterForm()
{

  $('#registerBoy').modal('toggle');

  var id_suffix = "";

  $("#profile_pic_v"+id_suffix).hide()
  $("#driving_liscence_pic_v"+id_suffix).hide()
  $("#pan_card_pic_v"+id_suffix).hide()
  $("#rc_pic_v"+id_suffix).hide()

  $("#exampleModalLabel").text("Create a Delivery Boy")
  $("#btn_add_agent").html("ADD AGENT")


}

function openDaOrderForm()
{

  $('#create_order_form_parent').modal('toggle');

  $("#exampleModalLabel").text("Create an Order")
  $("#btn_submit").html("Place Order")


}


function openDaRegisterCustomerCareForm()
{
  $('#registerBoy').modal('toggle');

  var id_suffix = "";

  $("#profile_pic_v"+id_suffix).hide()
  $("#driving_liscence_pic_v"+id_suffix).hide()
  $("#pan_card_pic_v"+id_suffix).hide()
  $("#rc_pic_v"+id_suffix).hide()

  $("#exampleModalLabel").text("Create a Customer Care Boy")
  $("#btn_add_agent").html("ADD AGENT")





}
// proceedEdit('jai1')
// getOrderDetails('XPHIY2X9')
function getOrderDetails(orderid)
{

 var csrftoken = getCookie('csrftoken');
 $.ajax({
        type: "POST",
        url: $("#order_fetch").val(),
        headers: {"X-CSRFToken": csrftoken},
        // url: "/get_da_details/",
        data: {order_id: orderid}, // serializes the form's elements.
        success: function(data)
        {
          // $( "#create_order_form_parent" ).load(location.href + " #create_order_form_parent" );

          $('#create_order_form_parent').modal('toggle');
            // alert(JSON.stringify(data)); // show response from the php script.
            if(data.SUCCESS)
             {

               // alert(JSON.stringify(data))
               final_data = JSON.parse(JSON.stringify(data))
               console.log(final_data);
               response_message = final_data.RESPONSE_MESSAGE
               data_order_meta = final_data.order_meta
               data_order_items = final_data.order_item
               data_customer_meta = final_data.user_customer.meta
               data_customer_profile = final_data.user_customer.profile[0]
               data_delivery_agent_meta = final_data.user_delivery_agent.meta
               data_delivery_agent_profile = final_data.user_delivery_agent.profile[0]



              // refresh div content


               $("#exampleModalLabel").text("Update an Order")
               $("#btn_submit").html("UPDATE ORDER")
               $("#pk").val(data_order_meta['order_id'])
               $("#username").val(data_customer_meta['username']);
               $("#phone_primary").val(data_customer_profile['phone_primary'])
               $("#location_city").val(data_customer_profile['location_city'])
               $("#location_locality").val(data_customer_profile['location_locality'])
               $("#location_area").val(data_customer_profile['location_area'])
               $("#location_sublocality").val(data_customer_profile['location_sublocality'])
               $("#location_pincode").val(data_customer_profile['location_pincode'])
               $("#location_state").val(data_customer_profile['location_pincode'])

               var state_key = data_customer_profile['location_state'];
               var state_key_val = "";
               console.log(state_key);

               var mapped_state = $('#location_state option').map(function() {
               var obj_state = {};
               obj_state[this.value] = this.textContent;
               // alert("came opt"+this.value)
               if(state_key == this.value)
                 {
                   // alert("came opts=="+this.value)
                   state_key_val = this.value;
                 }
               return obj_state;
             });

             $("#location_state").val(state_key_val)


             var lis = document.querySelectorAll('#ole li');
             for(var i=0; li=lis[i]; i++) {
                 if(i!=0)
                     li.parentNode.removeChild(li);
             }

             for (i = 0; i < data_order_items.length; i++) {

               if(i != data_order_items.length-1)
                  getOrderItemComponent()

               id = i+1
               id_suffix = i == 0? "": "_"+id

               $("#item_name"+id_suffix).val(data_order_items[i]["item_name"])
               $("#item_quantity"+id_suffix).val(data_order_items[i]["item_quantity"])
               $('#item_pk'+id_suffix).val(data_order_items[i]["order_item_id"])

               var measurement_unit = data_order_items[i]['measurement_unit'];
               var measurement_unit_val = "";
               console.log("unit "+measurement_unit);

                 var mapped_state = $('#measurement_unit option').map(function() {
                 var obj_state = {};
                 obj_state[this.value] = this.textContent;
                 // alert("came opt"+this.value)
                 if(measurement_unit == this.value)
                   {
                     // alert("came opts=="+this.value)
                     measurement_unit_val = this.value;
                   }
                 return obj_state;
               });
               console.log("measurement_unit_val "+measurement_unit_val);
               $("#measurement_unit"+id_suffix).val(measurement_unit_val)








             }


                }
            else
            {
              alert(JSON.stringify(data.ERRORS))
            }

        }
      });

}


function viewEachOrderDetail(orderid)
{

 var csrftoken = getCookie('csrftoken');
 $.ajax({
        type: "POST",
        url: $("#order_fetch").val(),
        headers: {"X-CSRFToken": csrftoken},
        // url: "/get_da_details/",
        data: {order_id: orderid}, // serializes the form's elements.
        success: function(data)
        {
          $('#order_view_alrt').modal('toggle');
            // alert(JSON.stringify(data)); // show response from the php script.
            if(data.SUCCESS)
             {


               // alert(JSON.stringify(data))
               final_data = JSON.parse(JSON.stringify(data))
               console.log(final_data);
               response_message = final_data.RESPONSE_MESSAGE
               data_order_meta = final_data.order_meta
               data_order_items = final_data.order_item
               data_customer_meta = final_data.user_customer.meta
               data_customer_profile = final_data.user_customer.profile[0]
               data_delivery_agent_meta = final_data.user_delivery_agent.meta
               data_delivery_agent_profile = final_data.user_delivery_agent.profile[0]




               // $("#item_name").val("")
               // $("#pk").val(data_order_meta['order_id'])
               console.log(data_customer_profile['location_area']);
               $("#customer_name_v").text(data_customer_meta['username']);
               $("#phone_primary_v").text(data_customer_profile['phone_primary'])
               $("#location_city_v").text(data_customer_profile['location_city'])
               $("#location_locality_v").text(data_customer_profile['location_locality'])
               $("#location_area_v").text(data_customer_profile['location_area'])
               $("#location_sublocality_v").text(data_customer_profile['location_sublocality'])
               $("#locality_pincode_v").text(data_customer_profile['location_pincode'])
               $("#user_delivery_agent_v").text(data_delivery_agent_meta['username'])


               var state_key = data_customer_profile['location_state'];
               var state_key_val = "";
               console.log(state_key);

               var mapped_state = $('#location_state option').map(function() {
               var obj_state = {};
               obj_state[this.value] = this.textContent;
               // alert("came opt"+this.value)
               if(state_key == this.value)
                 {
                   // alert("came opts=="+this.value)
                   state_key_val = this.textContent;
                 }
               return obj_state;
             });


               $("#location_state_v").text(state_key_val)



               var lis = document.querySelectorAll('#ole_view li');
               for(var i=0; li=lis[i]; i++) {
                   if(i!=0)
                       li.parentNode.removeChild(li);
               }

               for (i = 0; i < data_order_items.length; i++) {

                 if(i != data_order_items.length-1)
                    viewOrderItemComponent()

                id = i+1
                id_suffix = i == 0? "_v": "_v_"+id

                $("#item_name"+id_suffix).text(data_order_items[i]["item_name"])
                $("#item_quantity"+id_suffix).text(data_order_items[i]["item_quantity"])
                $("#measurement_unit"+id_suffix).text(data_order_items[i]["measurement_unit"])



               }




             }
            else
            {
              alert(JSON.stringify(data.ERRORS))
            }

        }
      });

}






function getDaDetails()
{
   // var csrftoken = document.cookie
   // print(csrftoken)
   // getCookie('csrftoken');
   var csrftoken = getCookie('csrftoken');
  $.ajax({
         type: "POST",
         url: $("#da_fetch").val(),
         headers: {"X-CSRFToken": csrftoken},
         // url: "/get_da_details/",
         data: {username:"Banu"}, // serializes the form's elements.
         success: function(data)
         {
           $('#registerBoyView').modal('toggle');
             // alert(JSON.stringify(data)); // show response from the php script.
             if(data.SUCCESS)
              {

                // alert(JSON.stringify(data))

                data_usermeta = JSON.parse(data.user_meta)[0]
                data_user_profile = JSON.parse(data.user_profile)[0]
                data_da_profile = JSON.parse(data.da_profile)[0]

                id_suffix = "";
                if(!(is_edit))
                id_suffix = "_v";
                // data_usermeta = data_json[0]
                // alert(JSON.stringify(data_usermeta))

                $("#pk"+id_suffix).val(data_usermeta.pk)
                $("#username"+id_suffix).val(data_usermeta.fields.username)
                $("#first_name"+id_suffix).val(data_usermeta.fields.first_name)
                $("#email"+id_suffix).val(data_usermeta.fields.email)

                $("#phone_primary"+id_suffix).val(data_user_profile.fields.phone_primary)
                $("#phone_secondary"+id_suffix).val(data_user_profile.fields.phone_secondary)
                $("#location_area"+id_suffix).val(data_user_profile.fields.location_area)
                $("#location_sublocality"+id_suffix).val(data_user_profile.fields.location_sublocality)
                $("#location_locality"+id_suffix).val(data_user_profile.fields.location_locality)
                $("#location_city"+id_suffix).val(data_user_profile.fields.location_city)
                $("#location_pincode"+id_suffix).val(data_user_profile.fields.location_pincode)


                // $("#profile_pic_v").src(data_user_profile.fields.profile_pic)
                var server_prefix = $("#pic_server_prefix").val();
                // alert(server_prefix+data_user_profile.fields.profile_pic);


                var state_key = data_user_profile.fields.location_state;
                var state_key_val = "";

                var mapped_state = $('#location_state option').map(function() {
                var obj_state = {};
                obj_state[this.value] = this.textContent;
                if(state_key == this.value)
                  state_key_val = this.textContent;
                return obj_state;
              });

// http://127.0.0.1:8000/media/

                $("#location_state"+id_suffix).val(state_key_val)


                $("#profile_pic_v"+id_suffix).attr("src",  server_prefix+data_user_profile.fields.profile_pic);
                $("#driving_liscence_pic_v"+id_suffix).attr("src",  server_prefix+data_da_profile.fields.driving_liscence_pic);
                $("#pan_card_pic_v"+id_suffix).attr("src", server_prefix+data_da_profile.fields.pan_card_pic);
                $("#rc_pic_v"+id_suffix).attr("src", server_prefix+data_da_profile.fields.rc_pic);



              }
             else
             {
               // alert(JSON.stringify(data.ERRORS))
             }

         }
       });

}


function updateOrderStatus(orderid){
  var selected_order_status = $('#order_status').find(":selected").text();
  console.log(selected_order_status);

  var csrftoken = getCookie('csrftoken');

  var url = $('#url_order_status').val()
  alert(url);

      $.ajax({
             type: "POST",
             url: url,
             headers: {"X-CSRFToken": csrftoken},
             data: {"order_status":selected_order_status, "order_id":orderid}, // serializes the form's elements.
             success: function(data)
             {
               alert(JSON.stringify(data))
              // processResponse(data)
             }
           });
}

function getUserOrderDetails(username){

  var csrftoken = getCookie('csrftoken');
  var url = $('#url_user_order_details').val()
  console.log(url);
  $.ajax({
         type: "POST",
         url: url,
         headers: {"X-CSRFToken": csrftoken},
         data: {"user_name":username}, // serializes the form's elements.
         success: function(data)
         {
           console.log("dsdsd");

           if(data.SUCCESS){

                alert(JSON.stringify(data));

                final_data = JSON.parse(JSON.stringify(data))
                response_message = final_data.RESPONSE_MESSAGE
                data_order_detail= final_data.user_order_detail

                if (data_order_detail.length == 0){
                  alert("Not yet orderd");

                }else {

                  $('#user_order_view_alrt').modal('toggle');

                  var lis = document.querySelectorAll('#item_table tr');
                  console.log(lis);
                  for(var i=0; tr=lis[i]; i++) {

                          tr.parentNode.removeChild(tr);
                  }

                  for(var i = 0; i< data_order_detail.length; i++){

                      userOrderListTable(i);
                      $('#order_id_'+i).html(data_order_detail[i]["order_id"]);
                      $('#order_item_'+i).html(data_order_detail[i]["item_name"]);
                      $('#created_at_'+i).html(new Date(data_order_detail[i]["created_at"]).toISOString().slice(0, 16));
                      $('#updated_at_'+i).html( new Date(data_order_detail[i]["updated_at"]).toISOString().slice(0, 16));

                    }
                }


           }else {

           }

        }
       });

}


function userOrderListTable(current_index){
  var html_content = '<tr>';
  html_content += '<td id="order_id_'+current_index+'" name="order_id_'+current_index+'" ></td>'
  html_content += '<td id="order_item_'+current_index+'" name="order_item_'+current_index+'" ></td>'
  html_content += '<td id="created_at_'+current_index+'" name="created_at_'+current_index+'" ></td>'
  html_content += '<td id="updated_at_'+current_index+'" name="updated_at_'+current_index+'" ></td>'
  html_content += '</tr>';
  $("#item_table").append(html_content);

}


function getOrderItemComponent()
{


  var count_order_items = $("#ole li").length;
  // alert(count_order_items);
  console.log(count_order_items);
  var current_index = count_order_items+1;

  var html_content = '<li>';
  html_content += '<div class="form-group col-md-8 pl_0 float-left">';
  html_content += '<label for="exampleInputEmail1">'+current_index+'. Items name / product name (ಉತ್ಪನ್ನದ ಹೆಸರು)</label>';
  html_content += '<input type="text" class="form-control" id="item_name_'+current_index+'" name="item_name_'+current_index+'" placeholder="Write down the requirment">';
  html_content += '</div>';
  html_content += '<div class="form-group col-md-2 pl_0 float-left">';
  html_content += '<label for="exampleInputEmail1">Quantity</label>';
  html_content += '<input type="number" class="form-control" id="item_quantity_'+current_index+'" value="1" name="item_quantity_'+current_index+'" placeholder="Quantity">';
  html_content += '</div>';
  html_content += '<div class="form-group col-md-2 pl_0 float-left">';
  html_content += '<label for="">UNIT</label>';
  html_content += '<select class="form-control" id="measurement_unit_'+current_index+'" name="measurement_unit_'+current_index+'">';
  var cont = document.getElementById("measurement_unit").innerHTML;
  html_content += cont;
  html_content += '</select>';
  html_content += '</div>';
  html_content+= '<input type="hidden" class="form-control" name="item_pk_'+current_index+'" id="item_pk_'+current_index+'"  placeholder="Order Item Id" >';
  html_content += '</li>';

   $("#ole").append(html_content);

}


function viewOrderItemComponent()
{


  var count_order_items = $("#ole_view li").length;
  // alert(count_order_items);
  console.log(count_order_items);
  var current_index = count_order_items+1;

  var html_content = '<li>';
  html_content += '<div class="form-group col-md-8 pl_0 float-left">';
  html_content += '<label for="exampleInputEmail1">'+current_index+'. Items name / product name (ಉತ್ಪನ್ನದ ಹೆಸರು)</label>';
  html_content += '<span class="font_14 float-left" id="item_name_v_'+current_index+'"> </span>';
  html_content += '</div>';
  html_content += '<div class="form-group col-md-2 pl_0 float-left">';
  html_content += '<label for="exampleInputEmail1">Quantity</label>';
  html_content += '<span class="font_14 float-left" id="item_quantity_v_'+current_index+'"></span>';
  html_content += '</div>';
  html_content += '<div class="form-group col-md-2 pl_0 float-left">';
  html_content += '<label for="">UNIT</label>';
  html_content += '<span class="font_14 float-left" id="measurement_unit_v_'+current_index+'"> </span>';
  html_content += '</div>';
  html_content += '</li>';

  $("#ole_view").append(html_content);

}
