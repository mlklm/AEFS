function validform() {
    var isValid = true;
    if (isEmpty(document.getElementById("fileToUpload").value)) {
        alert('Select a file !!');
        isValid = false;
    }
    if (!isCheck(document.getElementById("burnafterreading"))) {
        if (isEmpty(document.getElementById("pasteExpiration").value)) {
            alert('Set an expiration date !!');
            isValid = false;
        }
    }
    if (!isEmpty(document.getElementById("passphrase").value)) {
        if (!isMatch(document.getElementById("passphrase").value, document.getElementById("passphrase2").value)) {
            alert('Passphrase unmatch !!');
            isValid = false;
        }

    }
    return isValid;
}

function isEmpty(val) {
    return (typeof val === "undefined") || (val === "");
}

function isMatch(val, val2) {
    return val === val2;
}

function isCheck(elm) {
    return elm.checked;
}