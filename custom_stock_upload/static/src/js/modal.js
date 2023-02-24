odoo.define('custom_stock_upload.modal', function (require) {
'use strict';
        var ajax = require('web.ajax');
        var base64
        var modal = document.getElementById("myModal");
        var error = document.getElementById("error_div");
        var btn = document.getElementById("myBtn");
        var cancel_upload = document.getElementById("cancel_upload");
        var span = document.getElementsByClassName("close")[0];
        btn.onclick = function() {
          modal.style.display = "block";
        }
        span.onclick = function() {
          modal.style.display = "none";
        }
        cancel_upload.onclick = function() {
          modal.style.display = "none";
        }
        window.onclick = function(event) {
          if (event.target == modal) {
            modal.style.display = "none";
          }
        }
        $(document).on('click', '#upload_stocks', function () {
            var file = base64
            ajax.jsonRpc("/stck/upload", 'call',{'value': file}).then(function (result){
                if (result == true){
                    modal.style.display = "none";
                }else{
                    error.style.display = "block";
                }
        })
        })
        document.querySelector('#myfile').addEventListener('change',   function () {
            var reader = new FileReader();
            var selectedFile = this.files[0];
            reader.onload = function () {
                var comma = this.result.indexOf(',');
                base64 = this.result.substr(comma + 1);
            }
            reader.readAsDataURL(selectedFile);
        }, false);
});