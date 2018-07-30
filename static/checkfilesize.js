function checkFileSize(evt) {

    var oFile = document.getElementById("userimage").files[0]; 

                console.log(oFile.size); 

                if (oFile.size > 300000) {
                    evt.preventDefault();
                    alert("File size must under 3kb!");
                }

}