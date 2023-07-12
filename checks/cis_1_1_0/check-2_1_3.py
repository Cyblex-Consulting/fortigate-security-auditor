from checker import Checker

class Check_CIS_2_1_3(Checker):

    def __init__(self, firewall, display, verbose=False):
        
        super().__init__(firewall, display, verbose)

        self.id = "2.1.3"
        self.title = "Ensure timezone is properly configured"
        self.levels = [1]
        self.auto = False
        self.benchmark_version = "v1.1.0"
        self.benchmark_author = "CIS"

    def do_check(self):
        config_system_global = self.get_config("system global")

        if not "timezone" in config_system_global.keys():
            self.set_message("No timezone defined")
            return False

        timezone = config_system_global["timezone"]

        timezones = {
            "01":"(GMT-11:00) Midway Island, Samoa",
            "02":"(GMT-10:00) Hawaii",
            "03":"(GMT-9:00) Alaska",
            "04":"(GMT-8:00) Pacific Time (US & Canada)",
            "05":"(GMT-7:00) Arizona",
            "81":"(GMT-7:00) Baja California Sur, Chihuahua",
            "06":"(GMT-7:00) Mountain Time (US & Canada)",
            "07":"(GMT-6:00) Central America",
            "08":"(GMT-6:00) Central Time (US & Canada)",
            "09":"(GMT-6:00) Mexico City",
            "10":"(GMT-6:00) Saskatchewan",
            "11":"(GMT-5:00) Bogota, Lima,Quito",
            "12":"(GMT-5:00) Eastern Time (US & Canada)",
            "13":"(GMT-5:00) Indiana (East)",
            "74":"(GMT-4:00) Caracas",
            "14":"(GMT-4:00) Atlantic Time (Canada)",
            "77":"(GMT-4:00) Georgetown",
            "15":"(GMT-4:00) La Paz",
            "87":"(GMT-4:00) Paraguay",
            "16":"(GMT-3:00) Santiago",
            "17":"(GMT-3:30) Newfoundland",
            "18":"(GMT-3:00) Brasilia",
            "19":"(GMT-3:00) Buenos Aires",
            "20":"(GMT-3:00) Nuuk (Greenland)",
            "75":"(GMT-3:00) Uruguay",
            "21":"(GMT-2:00) Mid-Atlantic",
            "22":"(GMT-1:00) Azores",
            "23":"(GMT-1:00) Cape Verde Is.",
            "24":"(GMT) Monrovia",
            "80":"(GMT) Greenwich Mean Time",
            "79":"(GMT) Casablanca",
            "25":"(GMT) Dublin, Edinburgh, Lisbon, London, Canary Is.",
            "26":"(GMT+1:00) Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna",
            "27":"(GMT+1:00) Belgrade, Bratislava, Budapest, Ljubljana, Prague",
            "28":"(GMT+1:00) Brussels, Copenhagen, Madrid, Paris",
            "78":"(GMT+1:00) Namibia",
            "29":"(GMT+1:00) Sarajevo, Skopje, Warsaw, Zagreb",
            "30":"(GMT+1:00) West Central Africa",
            "31":"(GMT+2:00) Athens, Sofia, Vilnius",
            "32":"(GMT+2:00) Bucharest",
            "33":"(GMT+2:00) Cairo",
            "34":"(GMT+2:00) Harare, Pretoria",
            "35":"(GMT+2:00) Helsinki, Riga, Tallinn",
            "36":"(GMT+2:00) Jerusalem",
            "37":"(GMT+3:00) Baghdad",
            "38":"(GMT+3:00) Kuwait, Riyadh",
            "83":"(GMT+3:00) Moscow",
            "84":"(GMT+3:00) Minsk",
            "40":"(GMT+3:00) Nairobi",
            "85":"(GMT+3:00) Istanbul",
            "41":"(GMT+3:30) Tehran",
            "42":"(GMT+4:00) Abu Dhabi, Muscat",
            "43":"(GMT+4:00) Baku",
            "39":"(GMT+3:00) St. Petersburg, Volgograd",
            "44":"(GMT+4:30) Kabul",
            "46":"(GMT+5:00) Islamabad, Karachi, Tashkent",
            "47":"(GMT+5:30) Kolkata, Chennai, Mumbai, New Delhi",
            "51":"(GMT+5:30) Sri Jayawardenepara",
            "48":"(GMT+5:45) Kathmandu",
            "45":"(GMT+5:00) Ekaterinburg",
            "49":"(GMT+6:00) Almaty, Novosibirsk",
            "50":"(GMT+6:00) Astana, Dhaka",
            "52":"(GMT+6:30) Rangoon",
            "53":"(GMT+7:00) Bangkok, Hanoi, Jakarta",
            "54":"(GMT+7:00) Krasnoyarsk",
            "55":"(GMT+8:00) Beijing, ChongQing, HongKong, Urumgi, Irkutsk",
            "56":"(GMT+8:00) Ulaan Bataar",
            "57":"(GMT+8:00) Kuala Lumpur, Singapore",
            "58":"(GMT+8:00) Perth",
            "59":"(GMT+8:00) Taipei",
            "60":"(GMT+9:00) Osaka, Sapporo, Tokyo, Seoul",
            "62":"(GMT+9:30) Adelaide",
            "63":"(GMT+9:30) Darwin",
            "61":"(GMT+9:00) Yakutsk",
            "64":"(GMT+10:00) Brisbane",
            "65":"(GMT+10:00) Canberra, Melbourne, Sydney",
            "66":"(GMT+10:00) Guam, Port Moresby",
            "67":"(GMT+10:00) Hobart",
            "68":"(GMT+10:00) Vladivostok",
            "69":"(GMT+10:00) Magadan",
            "70":"(GMT+11:00) Solomon Is., New Caledonia",
            "71":"(GMT+12:00) Auckland, Wellington",
            "72":"(GMT+12:00) Fiji, Kamchatka, Marshall Is.",
            "00":"(GMT+12:00) Eniwetok, Kwajalein",
            "82":"(GMT+12:45) Chatham Islands",
            "73":"(GMT+13:00) Nuku'alofa",
            "86":"(GMT+13:00) Samoa",
            "76":"(GMT+14:00) Kiritimati"
        }

        question = 'Is the timezone ' + timezones[timezone] + ' correct? (Y/n)'

        answer = self.ask(question)
        
        if answer == 'n' or answer == 'N':
            self.set_message("Manually set to not compliant")
            return False
        else:
            self.set_message("Manually set to compliant")
            return True
