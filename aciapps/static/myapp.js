function applogin (){
    var window_TOKEN
    $.ajax('applogin.json', {
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
            'aaaUser': {
                'attributes': {
                    'name': 'admin',
                    'pwd': 'ciscopsdt'
                }
            }
        })
    })
    .done(function(response){
        window_TOKEN = response;
        console.log('login success')
        document.cookie = "APIC-Cookie=" + window_TOKEN;
        window.setInterval(remoteaci(window_TOKEN), 5000);
    })
    .fail(function(response){
        console.log('login fail');
    });
   // return window_TOKEN
};

function getportevents() {
    console.log('portevents')
    $.ajax('../static/portevents.json', {
        dataType: 'json',
        contentType: 'application/json',
        cache: false
    }).done(function(response){
        response = response['imdata'];
        console.log('hiiiiii')
        console.log(typeof response);
      //  record = event['eventRecord']['attributes']
  //      $.each(response, function(index, event){
  //          console.log('index: '+ index + '::' + event.eventRecord.attributes.cause)
  //          console.log(event['eventRecord']['attributes'].affected)
  //      })
    }).fail(function(response){
        console.log('fail getting port events')
    })
};

//window.ADDRESS = '198.18.133.200'
window.ADDRESS = 'sandboxapicdc.cisco.com';
window.ENTRY_POINT = 'https://' + window.ADDRESS;
var urladditional = '/api/node/class/eventRecord.json?query-target-filter=or(eq(eventRecord.cause,"port-up"),eq(eventRecord.cause,"port-down"),eq(eventRecord.cause,"port-pfc-congested"),eq(eventRecord.cause,"port-security-config-not-supported"),eq(eventRecord.cause,"update-remote-port-to-dbgrelem-failed"),eq(eventRecord.cause,"addor-del-uplink-port-group-failed"),eq(eventRecord.cause,"addor-del-vtep-port-group-failed"),eq(eventRecord.cause,"port-state-change"),eq(eventRecord.cause,"port-pfc-congested"))&order-by=eventRecord.created|desc&page=0&page-size=15'

function remoteaci(window_TOKEN) {
    console.log('remote server request')
    console.log('sending request to app.py')
  //  console.log(window_TOKEN)
    $.ajax('portevents.json', {
        type: 'GET',
        dataType: 'json',
        cache: false,
        contentType: 'application/json',
      //  headers: {
      //      'APIC-challenge' : window_TOKEN
      //  }
    }).done(function(response){
        console.log('success remote access');
        console.log(response);
        $.each(response.imdata, function(index, event){
            var short = event.eventRecord.attributes
         console.log(short.affected + " '" + short.descr + "'")
          //  console.log(event['eventRecord']['attributes'].affected)
        })
    }).fail(function(failrespone){
        console.log('failed cross domain request');
        console.log(failrespone);
    })
};

$(document).ready(function(){
    console.log('frontend ready')
    var window_TOKEN = applogin();
    getportevents();


});