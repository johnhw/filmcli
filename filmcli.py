import omdb
import textwrap
import colorama

def info(search):
    results = omdb.search(search)
    for i,r in enumerate(results):
        print "%d:%-50s [%s]\t %s" % (i,r.title, r.year, r.type)

def stars(x,y,nstars=10):
    try:
        x = float(x)
    except ValueError:
        return colorama.Style.DIM + "[%s]" % ("X"*nstars)
    float_rating = x/float(y)
    rating = (nstars * x) / float(y)
    int_rating = int(rating)
    partial_rating = rating - int_rating
    partial_map = [(0.0, '_'), (0.25, '~'), (0.5, '-'), (0.75, '^'), (1.0, "'")]
    i = 0    
    while partial_map[i][0]<partial_rating:
        i+=1
    partial_char = partial_map[i][1]    
    
    
    if float_rating<0.3:
        color = colorama.Back.RED + colorama.Fore.WHITE
    elif float_rating<0.5:
        color = colorama.Fore.RED + colorama.Back.BLACK
    elif float_rating<0.75:
        color = colorama.Fore.YELLOW + colorama.Back.BLACK
    elif float_rating<0.9:
        color = colorama.Fore.GREEN + colorama.Back.BLACK
    else:
        color = colorama.Back.GREEN + colorama.Fore.WHITE
    
    if int_rating==nstars:
        stars = "*"*nstars
    else:
        stars = ("*"*int_rating) + partial_char + (" "*(nstars-int_rating-1))
    return color+"[%s]" % stars+colorama.Fore.WHITE+colorama.Back.BLACK
        
def details(title):
    r = omdb.title(title, tomatoes=True)
    print
    print "-"*76
    print "%-51s %15s %3s [%s] %7s" % (colorama.Style.BRIGHT+r.title+colorama.Style.NORMAL, colorama.Fore.RED+r.rated+colorama.Fore.WHITE, r.runtime, colorama.Fore.GREEN+r.year+colorama.Fore.WHITE, r.type.upper())    
    
    print "%-21s" % (r.director)
    print "%-46s %s/%s" % (r.genre, r.country, r.language)
    print "-"*76
    print "%76s" % (r.actors)
    print
    if len(r.awards)>0:
        print colorama.Style.BRIGHT + "> " + r.awards + " <" + colorama.Style.NORMAL
    
    print
    print colorama.Fore.YELLOW + textwrap.fill(r.plot, width=76) + colorama.Fore.WHITE
    print
    print colorama.Fore.WHITE + textwrap.fill(r.tomato_consensus, width=76) + colorama.Fore.WHITE
    print
    print "     Meta  ", stars(r.metascore,100),    "     IMDB       ", stars(r.imdb_rating,10)
    print "     Tomato", stars(r.tomato_rating,10), "     Tomatometer", stars(r.tomato_meter,100)
    print "User Tomato", stars(r.tomato_user_rating,5), "User Tomatometer", stars(r.tomato_user_meter,100),
    print 
    
import sys    
if __name__=="__main__":
    colorama.init()
    title = " ".join(sys.argv[1:])
    details(title)