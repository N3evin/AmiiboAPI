var toastOptions = {
  "closeButton": true,
  "timeOut": 0,
  "extendedTimeOut": 0,
  "newestOnTop": true,
  "preventDuplicates": true,
  "positionClass": "toast-bottom-right"
};

var url = "/static/assets/notification.json";
var payload = $.getJSON(url)
  .done(function(data) {
    var notifcations = data.notifications;
    var index = 1;
    notifcations.forEach(function(data) {
      // Stack notification...
      if(data.type == "error"){
        setTimeout(function() {
          toastr.error(data.message, data.title, toastOptions);
        }, 1000 * index);
      } else if (data.type == "success"){
        setTimeout(function() {
          toastr.success(data.message, data.title, toastOptions);
        }, 1000 * index);
      } else if (data.type == "warning"){
        setTimeout(function() {
          toastr.warning(data.message, data.title, toastOptions);
        }, 1000 * index);
      } else {
        setTimeout(function() {
          toastr.info(data.message, data.title, toastOptions);
        }, 1000 * index);
      }
      index++;
    });
  })
  .fail(function(data) {
    toastr.error("failed", "Error", toastOptions);
  });

/**
 * https://github.com/CodeSeven/toastr
 * Requirement: Added jquery CDN and the CDN for toaster
 */