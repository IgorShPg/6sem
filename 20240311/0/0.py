import cmd
import calendar
import shlex



class Calendar(cmd.Cmd):
    prompt="CALENDAR-> "
    Months={c.name: c.value for c in calendar.Month}

    def do_prmonth(self, args):
        """give int year and month"""
        year, month=map(int, shlex.split(args)[0:2])
        calendar.TextCalendar().prmonth(year,month)

    def  do_pryear(self, args):
        """give int year"""
        year=int(shlex.split(args)[0])
        calendar.TextCalendar().pryear(year)

    def complete_prmonth(self, text, line, begidx, endidx):
        if len(line.split()) >= 2:
            return [c for c in self.Months if c.startswith(text)]

    









if __name__== "__main__":
    print(Calendar.Month)
    Calendar().cmdloop()
