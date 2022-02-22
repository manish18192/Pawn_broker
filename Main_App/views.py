from django.shortcuts import render
from datetime import datetime


# Create your views here.
def index(request):
    if request.method == 'POST':
        post_data = request.POST
        print(post_data)

        rate_below_5k = 3
        rate_above_5k = 2

        loan_date = post_data['Enter loan Date']
        loan_date = loan_date.split('-')
        release_date = post_data['Enter Release Date']
        release_date = release_date.split('-')

        if (int(release_date[2]) < int(loan_date[2])):
            release_date[2] = str(30 + int(release_date[2]))
            release_date[1] = str(int(release_date[1]) - 1)
        remeaning_days = int(release_date[2]) - int(loan_date[2])

        if (int(release_date[1]) < int(loan_date[1])):
            release_date[1] = str(12 + int(release_date[1]))
            release_date[0] = str(int(release_date[0]) - 1)
        remeaning_months = int(release_date[1]) - int(loan_date[1])

        remeaning_years = int(release_date[0]) - int(loan_date[0])

        amount = int(post_data['Enter Amount'])

        def si_cal(amount, rate_per_month, month, days):
            rate_mon_ = amount / 100 * rate_per_month
            months_si = month * rate_mon_
            day_si = rate_mon_ / 30 * days
            total_si = months_si + day_si
            return {
                'principal': amount,
                'month': month,
                'days': days,
                'monthly_si': months_si,
                'day_si': day_si,
                'si': total_si,
                'total': amount + total_si
            }



        rate_ = rate_below_5k
        if amount > 5000:
            rate_ = rate_above_5k

        # ci calculation of principal amount if duration is more than a year
        if remeaning_years >= 1:
            for x in range(remeaning_years):
                t_data = si_cal(amount=amount, rate_per_month=rate_, month=12, days=0)
                amount = t_data['total']

        # if not yearly duration then direct si else si calculation based on changed principal amount based on yearly ci
        data = si_cal(amount=amount, rate_per_month=rate_, month=remeaning_months, days=remeaning_days)
        data['year'] = remeaning_years
        print(data)
        return render(request, 'Result.html', context=data)

    return render(request, 'index.html')
