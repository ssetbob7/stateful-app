window.ADDRESS = 'sandboxapicdc.cisco.com';
window.ENTRY_POINT = 'https://' + window.ADDRESS;

/*function openSession(callback) {
    console.log('Opening session to ' + window.ADDRESS);
    $.ajax({
        type: 'POST',
        url: window.ENTRY_POINT + '/api/aaaLogin.json?gui-token-request=yes',
        dataType: 'json',
        success: function (results) {
            callback(results.imdata[0].aaaLogin.attributes);
        },
        error: function (responseData, textStatus, errorThrown) {
            console.error(responseData);
        },
        data: JSON.stringify({
            'aaaUser': {
                'attributes': {
                    'name': 'admin',
                    'pwd': 'C1sco12345'
                }
            }
        })
    });
}*/
/*var jsonaaa =  { 'aaaUser': 
    {'attributes': {
    'name': 'admin',
    'pwd': 'C1sco12345'
    }
}};*/
var jsonaaa = {'user':'admin', 'password':'ciscopsdt'}

function getFromApi(url, success, error) {
    var params = {
        type: 'GET',
        url: window.ENTRY_POINT + url,
        dataType: 'json',
        headers: {
            'DevCookie': window.TOKEN
        },
        success: function (results) {
            success(results)
            console.log("getfromapi: " + results)
        },
        error: function (results) {
            error(results)
        }
    }};

function listEndpoints(subnet, success, error) {
    console.log('Listing endpoints');
    getFromApi('/api/class/fvCEp.json?query-target-filter=wcard(fvCEp.ip,"2.2.2.0/24")&rsp-subtree=children', success, error);
}

function loginapi() {
    console.log('login');
    $.post('http://127.0.0.1:5000/applogin', jsonaaa, function(result){
    window.TOKEN = result
    var subnet = '2.2.2.0/24'
    console.log(result)
  //  listEndpoints(subnet, )
  //  })
})};

$(document).ready(function(){
//$(function () {
        console.log('Frontend is ready');
            loginapi()
            //openSession(function (aaaLoginAttributes) {
            //    console.log('Session is ready');
             //   window.TOKEN = aaaLoginAttributes.token;
              //  window.URL_TOKEN = aaaLoginAttributes.urlToken;
               // console.log(window.URL_TOKEN)
                //console.log(window.TOKEN)
         //   });
        });
