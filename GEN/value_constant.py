from GEN import dbconstants


KEY_LANGUAGE_TA = "TA"
KEY_LANGUAGE_EN = "EN"


KEY_D_SAVED_SUCCESSFULLY = "SAVED_SUCCESSFULLY"
KEY_D_BOOKING_FAILED = "BOOKING_FAILED"
KEY_D_PLEASE_TRY_AFTER_SOME_TIME = "PLEASE_TRY_AFTER_SOME_TIME"
KEY_D_SUCCESSFUL = "SUCCESSFUL"
KEY_D_BOOKING_REQUEST_CONFIRMATION = "BOOKING_REQUEST_CONFIRMATION"
KEY_D_BRANCH_OPERATIONAL_SELECTE_TIME = "BRANCH_OPERATIONAL_SELECTE_TIME"
KEY_D_SELECTE_TIME_BOOKED = "SELECTED_TIME_BOOKED"
KEY_D_LOGIN_SUCCESSFUL = "LOGIN_SUCCESSFUL"
KEY_D_ORDER_PLACED_SUCCESSFULLY = "ORDER_PLACED_SUCCESSFULLY"
KEY_D_BOOKING_NOT_CONFIRMED = "BOOKING_NOT_CONFIRMED"
KEY_D_TAP_TO_VIEW_DETAILS = "TAP_TO_VIEW_DETAILS"
KEY_D_BOOKING_CONFIRMED = "BOOKING_CONFIRMED"
KEY_D_ORDER_MARKED_AS_REJECTED = "ORDER_MARKED_AS_REJECTED"
KEY_D_ORDER_MARKED_AS_ACCEPTED = "ORDER_MARKED_AS_ACCEPTED"
KEY_D_ORDER_MARKED_AS_CHECKEDIN = "ORDER_MARKED_AS_CHECKEDIN"
KEY_D_ORDER_MARKED_AS_COMPLETED = "ORDER_MARKED_AS_COMPLETED"
KEY_D_NEW_REQUEST = "NEW_REQUEST"
KEY_D_NEW_BOOKING_REQUEST_VIEW_DETAILS = "NEW_BOOKING_REQUEST_VIEW_DETAILS"
KEY_D_USER_CREATED_SUCCESSFULLY = "USER_CREATED_SUCCESSFULLY"
KEY_D_INVALID_DATA = "INVALID_DATA"
KEY_D_NOT_INVALID_DATA ="NOT_INVALID_DATA"
KEY_D_BOOKING_SCHEDULED_REQUEST_TIME = "BOOKING_SCHEDULED_REQUEST_TIME"
KEY_D_ORDER_APPROVED = "ORDER_APPROVED"
KEY_D_ORDER_REJECTED = "ORDER_REJECTED"
KEY_D_NOT_REACHABLE = "NOT_REACHABLE"
KEY_D_ONGOING = "ONGOING"
KEY_D_COMPLETED = "COMPLETED"
KEY_D_PENDING_APPROVAL = "PENDING_APPROVAL"
KEY_D_SHOW_THE_QR_CODE_CHECK_IN = "SHOW_THE_QR_CODE_CHECK_IN"
KEY_D_AGENT_APPROVE = "AGENT_APPROVE"
KEY_D_NO_SLOT_AVAILABLE = "NO_SLOT_AVAILABLE "
KEY_D_NOT_OPERATING_REQUESTED_TIME = "NOT_OPERATING_REQUESTED_TIME "
KEY_D_CHECK_IN_APPOINTMENT = "CHECK_IN_APPOINTMENT "
KEY_D_APPOINTMENT_MARKED_AS_ONGOING = "APPOINTMENT_MARKED_AS_ONGOING "
KEY_D_BOOKING_MARKED_AS_COMPLETED = "BOOKING_MARKED_COMPLETED "




valueset = {
    KEY_D_SAVED_SUCCESSFULLY:{KEY_LANGUAGE_EN:"Saved Successfully", KEY_LANGUAGE_TA: "வெற்றிகரமாக சேமிக்கப்பட்டது"},
    KEY_D_BOOKING_FAILED:{KEY_LANGUAGE_EN: "Booking Failed", KEY_LANGUAGE_TA: "முன்பதிவு தோல்வியுற்றது"},
    KEY_D_PLEASE_TRY_AFTER_SOME_TIME: {KEY_LANGUAGE_EN: "Please try after some time.", KEY_LANGUAGE_TA: "சிறிது நேரம் கழித்து முயற்சிக்கவும்"},
    KEY_D_SUCCESSFUL: {KEY_LANGUAGE_EN: "Booking Request Placed", KEY_LANGUAGE_TA: "Booking Request Placed"},
    KEY_D_BOOKING_REQUEST_CONFIRMATION: {KEY_LANGUAGE_EN: "Booking Request Successful.Please wait for confirmation", KEY_LANGUAGE_TA: "முன்பதிவு கோரிக்கை வெற்றிகரமாக உள்ளது. உறுதிப்படுத்த காத்திருக்கவும்"},
    KEY_D_BRANCH_OPERATIONAL_SELECTE_TIME: {KEY_LANGUAGE_EN: "Branch not operational at selected time. Please try choosing some other time.",KEY_LANGUAGE_TA: "தேர்ந்தெடுக்கப்பட்ட நேரத்தில் கிளை செயல்படாது.எனவே மற்றொரு நேரத்தை தேர்ந்தெடுக்க முயற்சிக்கவும்."},
    KEY_D_SELECTE_TIME_BOOKED:{KEY_LANGUAGE_EN:"Selected time is booked. Please try choosing some other time.", KEY_LANGUAGE_TA:"இந்த நேரம் ஏற்கனவே முன்பதிவு செய்யப்பட்டுள்ளது, எனவே மற்றொரு நேரத்தைத் தேர்வுசெய்க"},
    KEY_D_LOGIN_SUCCESSFUL:{KEY_LANGUAGE_EN:"Login Successful", KEY_LANGUAGE_TA:"உள்நுழைவு வெற்றிகரமாக முடிந்தது"},
    KEY_D_ORDER_PLACED_SUCCESSFULLY: {KEY_LANGUAGE_EN: "Order Placed Successfully", KEY_LANGUAGE_TA: "ஆர்டர் வெற்றிகரமாக சேர்க்கப்பட்டுள்ளது "},
    KEY_D_BOOKING_NOT_CONFIRMED: {KEY_LANGUAGE_EN: "Booking not Confirmed",KEY_LANGUAGE_TA: "முன்பதிவு உறுதிப்படுத்தப்படவில்லை"},
    KEY_D_TAP_TO_VIEW_DETAILS: {KEY_LANGUAGE_EN: "Tap to view details",KEY_LANGUAGE_TA: "விவரங்களைக் காண தட்டவும்"},
    KEY_D_BOOKING_CONFIRMED: {KEY_LANGUAGE_EN:"Booking Confirmed", KEY_LANGUAGE_TA: "முன்பதிவு உறுதி செய்யப்பட்டது"},
    KEY_D_ORDER_MARKED_AS_REJECTED: {KEY_LANGUAGE_EN: "Order Marked as Rejected", KEY_LANGUAGE_TA: "ஆர்டர் நிராகரிக்கப்பட்டது எனக் குறிக்கப்பட்டுள்ளது"},
    KEY_D_ORDER_MARKED_AS_ACCEPTED: {KEY_LANGUAGE_EN: "Order Marked as Accepted", KEY_LANGUAGE_TA: "ஆர்டர் ஏற்றுக்கொள்ளப்பட்டதாகக் குறிக்கப்பட்டுள்ளது"},
    KEY_D_ORDER_MARKED_AS_CHECKEDIN: {KEY_LANGUAGE_EN: "Order Marked as Checked In", KEY_LANGUAGE_TA: "ஆர்டர் செக்-இன் எனக் குறிக்கப்பட்டது"},
    KEY_D_ORDER_MARKED_AS_COMPLETED: {KEY_LANGUAGE_EN: "Order Marked as Completed", KEY_LANGUAGE_TA: "ஆர்டர் முடிந்தது எனக் குறிக்கப்பட்டுள்ளது"},
    KEY_D_NEW_REQUEST: {KEY_LANGUAGE_EN: "New Request", KEY_LANGUAGE_TA: "புதிய கோரிக்கை"},
    KEY_D_NEW_BOOKING_REQUEST_VIEW_DETAILS: {KEY_LANGUAGE_EN: "There is a new booking request.Tap to view details", KEY_LANGUAGE_TA: "புதிய முன்பதிவு கோரிக்கைக்கான விவரங்களைக் காண தட்டவும்"},
    KEY_D_USER_CREATED_SUCCESSFULLY: {KEY_LANGUAGE_EN: "User Created Successfully", KEY_LANGUAGE_TA: "பயன்பாட்டாளர் வெற்றிகரமாக உருவாக்கப்பட்டது"},
    KEY_D_INVALID_DATA: {KEY_LANGUAGE_EN: "INVALID DATA", KEY_LANGUAGE_TA: "தவறான தகவல்கள்"},
    KEY_D_NOT_INVALID_DATA: {KEY_LANGUAGE_EN: "Not a valid data", KEY_LANGUAGE_TA: "சரியான தகவல்கள் அல்ல"},
    KEY_D_BOOKING_SCHEDULED_REQUEST_TIME: {KEY_LANGUAGE_EN:"Booking confirmed and the slot has been scheduled on requested time",KEY_LANGUAGE_TA: "முன்பதிவு உறுதிசெய்யப்பட்டது மற்றும் கேட்கப்பட்ட நேரத்தில்  திட்டமிடப்பட்டுள்ளது"},
    KEY_D_ORDER_APPROVED: {KEY_LANGUAGE_EN:"Order Approved", KEY_LANGUAGE_TA: "ஆர்டர் அங்கீகரிக்கப்பட்டது"},
    KEY_D_ORDER_REJECTED: {KEY_LANGUAGE_EN: "Order Rejected", KEY_LANGUAGE_TA: "ஆர்டர் நிராகரிக்கப்பட்டது"},
    KEY_D_NOT_REACHABLE: {KEY_LANGUAGE_EN: "Not Reachable", KEY_LANGUAGE_TA:"தொடர்பு கொள்ள முடியவில்லை"},
    KEY_D_ONGOING: {KEY_LANGUAGE_EN: "Ongoing", KEY_LANGUAGE_TA: "நடந்து கொண்டிருக்கிறது"},
    KEY_D_COMPLETED: {KEY_LANGUAGE_EN:  "Completed", KEY_LANGUAGE_TA: "நிறைவுபெற்றது"},
    KEY_D_PENDING_APPROVAL: {KEY_LANGUAGE_EN: "Pending Approval", KEY_LANGUAGE_TA: "ஒப்புதல் நிலுவையில் உள்ளது"},
    KEY_D_SHOW_THE_QR_CODE_CHECK_IN: {KEY_LANGUAGE_EN: "Show the QR Code for easy check-in", KEY_LANGUAGE_TA: "எளிதாக சரிபார்க்க QR குறியீட்டைக் காட்டுக"},
    KEY_D_AGENT_APPROVE: {KEY_LANGUAGE_EN: "Please be patient. the agent will approve shortly.", KEY_LANGUAGE_TA: "தயவுசெய்து பொறுமையாக இருங்கள். முகவர் விரைவில் ஒப்புக்கொள்வார்."},
    KEY_D_NO_SLOT_AVAILABLE: {KEY_LANGUAGE_EN: "No slot available", KEY_LANGUAGE_TA: "ஸ்லாட் கிடைக்கவில்லை"},
    KEY_D_NOT_OPERATING_REQUESTED_TIME: {KEY_LANGUAGE_EN: "Not operating in requested time", KEY_LANGUAGE_TA: "கேட்கப்பட்ட நேரத்தில் இயங்கவில்லை"},
    KEY_D_CHECK_IN_APPOINTMENT: {KEY_LANGUAGE_EN: "You have not checked-In for the Appointment", KEY_LANGUAGE_TA:"நீங்கள் சந்திப்புக்கு செக்-இன் செய்யவில்லை"},
    KEY_D_APPOINTMENT_MARKED_AS_ONGOING: {KEY_LANGUAGE_EN: "Appointment marked as Ongoing", KEY_LANGUAGE_TA: "நியமனம் நடப்பதாக குறிக்கப்பட்டுள்ளது"},
    KEY_D_BOOKING_MARKED_AS_COMPLETED: {KEY_LANGUAGE_EN: "Booking has been marked as completed", KEY_LANGUAGE_TA:"முன்பதிவு முடிந்ததாக குறிக்கப்பட்டுள்ளது"},


}


def get_display_translated_value(key, language = KEY_LANGUAGE_EN):
    try:
        return valueset[key][language]
    except:
        return ""




def get_string_value_by_user(key, user_id = dbconstants.USER_ID_DEFAULT):
    language = KEY_LANGUAGE_EN

    try:
        return valueset[key][language]
    except:
        return ""


def get_string_value_by_lang(key, language = KEY_LANGUAGE_EN):

    try:
        return valueset[key][language]
    except:
        return ""






