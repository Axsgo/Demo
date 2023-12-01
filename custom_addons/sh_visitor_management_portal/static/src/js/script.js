$(document).ready(function () {
    $("#create_visitor_btn").click(function () {
        $("#create_visitor").modal("show");
        var date = new Date();
        var get_date = date.getDate();
        var get_month = date.getMonth() + 1;
        var get_month_str = String(get_month);
        if (get_month_str.length == 1) {
            var get_month_str = "0" + String(get_month);
        }
        var get_year = date.getFullYear();
        var hours = date.getHours();
        var minutes = date.getMinutes();
        var ampm = hours >= 12 ? "PM" : "AM";
        hours = hours % 12;
        hours = hours ? hours : 12;
        minutes = minutes < 10 ? "0" + minutes : minutes;
        var strTime = get_month_str + "/" + get_date + "/" + get_year + " " + hours + ":" + minutes + " " + ampm;
        $("#check_in").val(strTime);
    });
    $.ajax({
        url: "/get-partner-details",
        data: {
            partner_id: $("#partner_id").val(),
        },
        type: "post",
        cache: false,
        success: function (result) {
            var datas = JSON.parse(result);
            $("#visitor_name").val(datas.visitor_name);
            $("#visitor_company").val(datas.company);
            $("#phone").val(datas.phone);
            $("#mobile").val(datas.mobile);
            $("#email").val(datas.email);
        },
    });

    $("#employee_id").change(function () {
        $.ajax({
            url: "/get-employee-details",
            data: {
                employee_id: $("#employee_id").val(),
            },
            type: "post",
            cache: false,
            success: function (result) {
                var datas = JSON.parse(result);
                $("#department_id").val(datas.department_id);
            },
        });
    });
    $("#submit_btn").click(function () {
        $.ajax({
            url: "/create-visit",
            data: {
                partner_id: $("#partner_id").val(),
                check_in: $("#check_in").val(),
                visitor_name: $("#visitor_name").val(),
                check_out: $("#check_out").val(),
                company: $("#visitor_company").val(),
                phone: $("#phone").val(),
                mobile: $("#mobile").val(),
                mail: $("#email").val(),
                destination_id: $("#visit_dest_id").val(),
                visit_type_id: $("#visit_type_id").val(),
                visit_categ_id: $("#visit_categ_id").val(),
                reference: $("#reference").val(),
                employee_id: $("#employee_id").val(),
                department: $("#department_id").val(),
                purpose: $("#purpose").val(),
            },
            type: "post",
            cache: false,
            success: function (result) {
                var datas = JSON.parse(result);
                if (datas.error) {
                    alert(datas.error);
                } else {
                    window.location.href = datas.url;
                }
            },
        });
    });
    $("#partner_id").change(function () {
        $.ajax({
            url: "/get-partner-details",
            data: {
                partner_id: $("#partner_id").val(),
            },
            type: "post",
            cache: false,
            success: function (result) {
                var datas = JSON.parse(result);
                $("#visitor_name").val(datas.visitor_name);
                $("#visitor_company").val(datas.company);
                $("#phone").val(datas.phone);
                $("#mobile").val(datas.mobile);
                $("#email").val(datas.email);
            },
        });
    });
    $("#employee_id").change(function () {
        $.ajax({
            url: "/get-employee-details",
            data: {
                employee_id: $("#employee_id").val(),
            },
            type: "post",
            cache: false,
            success: function (result) {
                var datas = JSON.parse(result);
                $("#department_id").val(datas.department_id);
            },
        });
    });
    $("#check_in").focusout(function () {
        $.ajax({
            url: "/get-duration",
            data: {
                check_in: $("#check_in").val(),
                check_out: $("#check_out").val(),
            },
            type: "post",
            cache: false,
            success: function (result) {
                var datas = JSON.parse(result);
                if (datas.error) {
                    alert(datas.error);
                } else {
                    $("#duration").val(datas.duration);
                }
            },
        });
    });
    $("#check_out").focusout(function () {
        $.ajax({
            url: "/get-duration",
            data: {
                check_in: $("#check_in").val(),
                check_out: $("#check_out").val(),
            },
            type: "post",
            cache: false,
            success: function (result) {
                var datas = JSON.parse(result);
                $("#duration").val(datas.duration);
            },
        });
    });
    $(".check_out_btn").click(function (e) {
        var self = this;
        var $el = $(e.target).parents("tr").find("#visitor_id").attr("value");
        var visitor_id = parseInt($el);
        $.ajax({
            url: "/default-checkout",
            data: {
                visitor_id: visitor_id,
            },
            type: "post",
            cache: false,
            success: function (result) {
                var datas = JSON.parse(result);
                if (datas.success == 1) {
                    location.reload(true);
                }
            },
        });
    });
    $("#form_partner_id").change(function () {
        $.ajax({
            url: "/get-partner-details",
            data: {
                partner_id: $("#form_partner_id").val(),
            },
            type: "post",
            cache: false,
            success: function (result) {
                var datas = JSON.parse(result);
                $("#form_visitor_name").val(datas.visitor_name);
                $("#form_company").val(datas.company);
                $("#form_phone").val(datas.phone);
                $("#form_mobile").val(datas.mobile);
                $("#form_mail").val(datas.email);
            },
        });
    });
    $("#form_check_in").focusout(function () {
        $.ajax({
            url: "/get-duration",
            data: {
                check_in: $("#form_check_in").val(),
                check_out: $("#form_check_out").val(),
            },
            type: "post",
            cache: false,
            success: function (result) {
                var datas = JSON.parse(result);
                if (datas.error) {
                    alert(datas.error);
                } else {
                    $("#form_duration").text(datas.duration);
                }
            },
        });
    });
    $("#form_check_out").focusout(function () {
        $.ajax({
            url: "/get-duration",
            data: {
                check_in: $("#form_check_in").val(),
                check_out: $("#form_check_out").val(),
            },
            type: "post",
            cache: false,
            success: function (result) {
                var datas = JSON.parse(result);
                if (datas.error) {
                    alert(datas.error);
                } else {
                    $("#form_duration").text(datas.duration);
                }
            },
        });
    });

    $("#save_btn").click(function () {
        $.ajax({
            url: "/update-visitor-details",
            data: {
                visitor_id: $("#form_visitor_id").val(),
                visitor_name: $("#form_visitor_name").val(),
                comapny: $("#form_company").val(),
                phone: $("#form_phone").val(),
                mobile: $("#form_mobile").val(),
                mail: $("#form_mail").val(),
                check_in: $("#form_check_in").val(),
                check_out: $("#form_check_out").val(),
                duration: $("#form_duration").val(),
                reference: $("#form_reference").val(),
                partner_id: $("#form_partner_id").val(),
                destination_id: $("#form_destination_id").val(),
                visit_type_id: $("#form_visit_type_id").val(),
                visit_categ_id: $("#form_visit_categ_id").val(),
                employee_id: $("#form_employee_id").val(),
                purpose: $("#form_purpose").val(),
            },
            type: "post",
            cache: false,
            success: function (result) {
                var datas = JSON.parse(result);
                if (datas.success == 1) {
                    $("#save_btn").addClass("o_hidden");
                    $("#edit_btn").removeClass("o_hidden");
                    $("#form_visitor_name").attr("readonly", true);
                    $("#form_company").attr("readonly", true);
                    $("#form_phone").attr("readonly", true);
                    $("#form_mobile").attr("readonly", true);
                    $("#form_mail").attr("readonly", true);
                    $("#form_check_in").attr("readonly", true);
                    $("#form_check_out").attr("readonly", true);
                    $("#form_duration").attr("readonly", true);
                    $("#form_reference").attr("readonly", true);
                    $("#form_reference").attr("readonly", true);
                    $("#form_partner_id").attr("disabled", true);
                    $("#form_destination_id").attr("disabled", true);
                    $("#form_visit_type_id").attr("disabled", true);
                    $("#form_visit_categ_id").attr("disabled", true);
                    $("#form_employee_id").attr("disabled", true);
                    $("#form_purpose").attr("readonly", true);
                }
            },
        });
    });
    $("#edit_btn").click(function () {
        $("#save_btn").removeClass("o_hidden");
        $("#edit_btn").addClass("o_hidden");
        $("#form_visitor_name").attr("readonly", false);
        $("#form_company").attr("readonly", false);
        $("#form_phone").attr("readonly", false);
        $("#form_mobile").attr("readonly", false);
        $("#form_mail").attr("readonly", false);
        $("#form_check_in").attr("readonly", false);
        $("#form_check_out").attr("readonly", false);
        $("#form_reference").attr("readonly", false);
        $("#form_reference").attr("readonly", false);
        $("#form_partner_id").attr("disabled", false);
        $("#form_destination_id").attr("disabled", false);
        $("#form_visit_type_id").attr("disabled", false);
        $("#form_visit_categ_id").attr("disabled", false);
        $("#form_employee_id").attr("disabled", false);
        $("#form_purpose").attr("readonly", false);
    });
    $(".js_cls_edit_pass").click(function (e) {
        var self = this;
        var $el = $(e.target).parents("tr").find("#visitor_id").attr("value");
        var visitor_id = parseInt($el);
        var joint_str = "/my/visitor/" + String(visitor_id) + "?edit=True";
        window.open(joint_str, "_self");
    });

    currLoc = $(location).attr("href");
    if (currLoc.includes("?")) {
        var split_str = currLoc.split("?");
        for (x in split_str) {
            if (split_str[x] == "edit=True") {
                $("#save_btn").removeClass("o_hidden");
                $("#edit_btn").addClass("o_hidden");
                $("#form_visitor_name").attr("readonly", false);
                $("#form_company").attr("readonly", false);
                $("#form_phone").attr("readonly", false);
                $("#form_mobile").attr("readonly", false);
                $("#form_mail").attr("readonly", false);
                $("#form_check_in").attr("readonly", false);
                $("#form_check_out").attr("readonly", false);
                $("#form_duration").attr("readonly", false);
                $("#form_reference").attr("readonly", false);
                $("#form_reference").attr("readonly", false);
                $("#form_partner_id").attr("disabled", false);
                $("#form_destination_id").attr("disabled", false);
                $("#form_visit_type_id").attr("disabled", false);
                $("#form_visit_categ_id").attr("disabled", false);
                $("#form_employee_id").attr("disabled", false);
                $("#form_purpose").attr("readonly", false);
            }
        }
    }
});
