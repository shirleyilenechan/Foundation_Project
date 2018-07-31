function checkFileSize(evt) {

    var oFile = document.getElementById("userimage").files[0]; 


                if (oFile.size > 300000) {
                    evt.preventDefault();
                    alert("File Size Must Under 3kb!");
                }

                if (!oFile.name.match(/.(jpg|jpeg|png)$/i)) {
                    evt.preventDefault();
                    alert('Not a Valid Image File');

                }

}
