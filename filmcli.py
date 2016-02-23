import omdb
import textwrap
import colorama

def stars(x,y,nstars=10):
    """Generate a color-coded star rating from an x/y rating.
    Uses trailing characters to represent fractional ratings:
    Ratings are _ ~ - ^ ': 0.2, 0.4, 0.6, 0.8
    """    
    try:
        x = float(x)
    except ValueError:
        return colorama.Style.DIM + "[%s]" % ("X"*nstars)
    float_rating = x/float(y)
    rating = (nstars * x) / float(y)
    int_rating = int(rating)
    partial_rating = rating - int_rating
    partial_map = [(0.2, '_'), (0.4, '~'), (0.6, '-'), (0.8, '^'), (1.0, "'")]
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
    
class ASCIIProxy(object):
        def __init__(self, obj):
            self.obj = obj
            
        def __getattr__(self, attr):
            val = getattr(self.obj, attr)                        
            if type(val)==type(u""):                
                return val.encode('ascii', 'ignore')
            else:
                return val    
        
def details(title):
    """Print the details of the given film (specified by title) to the console"""
    rf = omdb.title(title, tomatoes=True)
    
                
    r = ASCIIProxy(rf)
    print
    print "-"*76
    print "%s %15s %3s [%s] %7s" % (colorama.Fore.BLACK + colorama.Back.WHITE+("%-51s"%r.title)+colorama.Back.BLACK + colorama.Fore.WHITE, colorama.Fore.RED+r.rated+colorama.Fore.WHITE, r.runtime, colorama.Fore.GREEN+r.year+colorama.Fore.WHITE, r.type.upper())    
    
    print "%-21s" % (colorama.Style.BRIGHT + r.director + colorama.Style.NORMAL )
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

def interactive_mode():    
    results = []
    while  True:
        title = raw_input("> ")
        try:
            index = int(title)
            if index>=0 and index<len(results):
                details(results[index].title)
            else:
                print "?"
        except ValueError:
            results = omdb.search(title)
            for i,r in enumerate(results):
                rf = ASCIIProxy(r)
                print "%d: %20s   %4s" % (i, rf.title, rf.year)
        
    


if __name__=="__main__":
    colorama.init()    
    if "-i" in sys.argv:
        interactive_mode()
    else:
        title = (sys.argv[1:])    
        details(title)