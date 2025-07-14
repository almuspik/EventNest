from django.shortcuts import render, redirect,  get_object_or_404, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime 
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from .models import Event, Venue
from django.contrib.auth.models import User #usermodel
from .forms import VenueForm, EventForm, EventFormAdmin
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter 
from django.contrib import messages
#pagination imports
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#show events
def show_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'show_event.html', {'event': event})


def venue_events(request, venue_id):
    #grab venues and evens from that venue
    venue = Venue.objects.get(id=venue_id)
    events = venue.event_set.all()
    if events:
        return render(request, 'venue_events.html', {'events': events})
    else:
        messages.success(request,("There Is No Events In This Venue"))
        return redirect('admin_approval')


def admin_approval(request):
# get the venues
    venue_list = Venue.objects.all()

    # getting counts
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()
    event_list = Event.objects.all().order_by("-event_date")
    if request.user.is_superuser:
        if request.method == "POST":
            id_list = request.POST.getlist('boxes')
            # print(id_list)
            # uncheck all avents
            event_list.update(approved=False)
            # updatethe db
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)


            messages.success(request,( "Approval Status Is Updated"))
            return redirect('list-events')


        else:
            return render(request, 'admin_approval.html',{"event_list":event_list, "event_count":event_count, "venue_count":venue_count, "user_count":user_count, "venue_list":venue_list, })

    else:
        messages.success(request,( "You are not authorized to view this page"))
        return redirect('home')

    




def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=request.user.id)
        return render(request, 'my_events.html', {'events':events})
      

    else:
        messages.success(request, ("You Can't view this page"))
        return redirect('home')




def venue_pdf(request):
    buf = io.BytesIO()#bytsream buffer
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob= c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
      #designate the model
    venues = Venue.objects.all()

    lines= []

    for venue in venues:
        lines.append(f"Venue: {venue.name}")
        lines.append(f"Address: {venue.address}")
        lines.append(f"Zip Code: {venue.zip_code}")
        lines.append(f"Phone: {venue.phone}")
        lines.append(f"Website: {venue.web}")
        lines.append(f"Email: {venue.email_address}")
        lines.append("")
        lines.append("==========================================") 
        lines.append("")

    for line in lines:
        textob.textLine(line)
        
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename="venues.pdf")

def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="venues.csv"'
    #create a csv writer
    writer = csv.writer(response)
    #designate the model
    venues = Venue.objects.all()
    #Add column heading to the csv file 
    writer.writerow(['Venue Name', 'Address', 'Zip code', 'Phone', ' Web Address', 'Email Address'])
    
    #loop
    for venue in venues:
       writer.writerow([
        venue.name, 
        venue.address, 
        venue.phone, 
        venue.zip_code, 
        venue.web,
        venue.email_address]
    )
    return response


def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="venues.txt"'
    #designate the model
    venues = Venue.objects.all()
    line = []
    #loop
    for venue in venues:
        line.append(
        f"Venue: {venue.name}\n"
        f"Venue Location: {venue.address}\n"
        f"Phone: {venue.phone}\n"
        f"Zipcode: {venue.zip_code}\n"
        f"Web: {venue.web}\n"
        f"Email: {venue.email_address}\n\n"
    )# lines = ["This is line 1\n",
    #  "This is line 2\n", "this is line 3\n"]
    response.writelines(line)
    return response


def delete_venue(request, venue_id):
    venue= Venue.objects.get(pk=venue_id)

    venue.delete()
    return redirect('list-venues')

def delete_event(request, event_id):
    from django.shortcuts import get_object_or_404
    event = get_object_or_404(Event, pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, ("Event Deleted!!!!"))
        return redirect('list-events')

    else:
        messages.success(request, ("Manager can only delete the Event!!!"))
        return redirect('list-events')
    
def update_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        return redirect('list-events') 

    return render(request, 'update_events.html', {
        'event': event,
        'form': form
    })



def add_event(request):
    submitted= False
    if request.method=="POST":
        if request.user.is_superuser:
            form=EventFormAdmin(request.POST)
            if form.is_valid():
                event = form.save()
                event.manager = request.user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')

        else:
            form=EventForm(request.POST)
            if form.is_valid():
                #form.save()
                event = form.save(commit=False)
                event.manager = request.user# looged in user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        #just going to the page, not submiting
        if request.user.is_superuser:
              form=EventFormAdmin
    
        else:
              form=EventForm
        form=EventForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_events.html',{'form': form, 'submitted':submitted})



def update_venues(request, venue_id):
    venue= Venue.objects.get(pk=venue_id)
    venue_list= Venue.objects.all() 
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues') 
    return render(request, 'update_venues.html',{'venue':venue, 'form':form }) 


def search_events(request):
    if request.method == "POST":
        searched = request.POST['searched']
        
        events = Event.objects.filter(name__icontains=searched)

        return render(request, 'search_event.html', {
            'searched': searched,
            'events': events
        })

    return render(request, 'search_event.html', {})




def search_venues(request):
    if request.method == "POST":
        searched = request.POST['searched']
        
        venues = Venue.objects.filter(name__icontains=searched)

        return render(request, 'search_venues.html', {
            'searched': searched,
            'venues': venues
        })

    return render(request, 'search_venues.html', {})

def show_venues(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)

    venue_list= Venue.objects.all() 
    events = venue.event_set.all()


    return render(request, 'show_venues.html',{'venue':venue, 'venue_owner':venue_owner , 'events':events}) 

# def list_venues(request):
#     # venue_list= Venue.objects.all().order_by('name')
#     venue_list= Venue.objects.all()
#     #setup paginations
#     p = Paginator(Venue.objects.all(),2)
#     page = request.GET.get('page')
#     venues = p.get_page(page)
#     nums= "a" * venues.paginator.num_pages
#     try:
#         page_obj = Paginator.page(page_number)
#     except PageNotAnInteger:
#         page_obj = Paginator.page(1)  # If page is not an integer, show first page
#     except EmptyPage:
#         page_obj = Paginator.page(paginator.num_pages)  # If page out of range, show last page

#     return render(request, 'venues.html',{'venue_list':venue_list,
#      'venues' :venues, 'nums':nums})








def list_venues(request):
    venue_list = Venue.objects.all().order_by('name')
    paginator = Paginator(venue_list, 5)  # 2 venues per page

    page = request.GET.get('page')
    venues = paginator.get_page(page)  # ✅ This will never raise EmptyPage

    return render(request, 'venues.html', {
        'venues': venues,
    })




def add_venue(request):
    submitted= False
    if request.method=="POST":
        form=VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id # looged in user
            venue.save()
            # form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form=VenueForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_venues.html',{'form': form, 'submitted':submitted})



def all_events(request):
    events_list= Event.objects.all().order_by('-event_date')
    return render(request, 'events_list.html',{'events_list':events_list})



# def home(request, year=datetime.now().year , month=datetime.now().month):
#     name="Almuspik"
#     #Convert month from name to number
#     month = month.capitalize()
#     month_number = list(calendar.month_name).index(month)
#     month_number = int(month_number)
#     #create calendar
#     cal = HTMLCalendar().formatmonth(
#         year,
#         month_number
#     )

#     #current year
#     now = datetime.now()
#     current_year = now.year

#     time = now.strftime('%I:%M:%S %p').lower()


#     return render(request, 'home.html',
#         {
#         "First_name" :name,
#         "Year": year,
#         "month":month ,
#         "month_number":month_number,
#         "cal":cal,
#         "current_year": current_year,
#         "time": time,
        
#          })
def home(request, year=None, month=None):
    name = "Almuspik"

    now = datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.strftime('%B')  # gives full month name like "June"
    
    # Ensure month is capitalized string
    month = str(month).capitalize()

    try:
        month_number = list(calendar.month_name).index(month)
    except ValueError:
        return render(request, '404.html', status=404)  # Optional error handling

    # Create calendar
    cal = HTMLCalendar().formatmonth(year, month_number)


    # Query the events model for dates
    event_list = Event.objects.filter( event_date__year= year,
                                        event_date__month= month_number )


    # Current time
    time = now.strftime('%I:%M:%S %p').lower()

    return render(request, 'home.html', {
        "First_name": name,
        "Year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": now.year,
        "time": time,
        "event_list": event_list,
    })
