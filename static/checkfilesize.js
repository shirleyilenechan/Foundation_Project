var oFile = document.getElementById("userimage").files[0]; 

            if (oFile.size > 3000) {
                evt.preventDefault();
                alert("File size must under 3kb!");
            }