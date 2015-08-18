from glob import glob
import cv2

# Show resized image in resized window and wait for keyEvent to close
def showScaled(img, title='dupa', scale=0.5, saveName = None):
    small = cv2.resize(img, (0,0), fx=scale, fy=scale)
    cv2.imshow(title, small)
    cv2.waitKey()
    cv2.destroyAllWindows()
    if saveName is not None:
        cv2.imwrite(saveName, img)

def nothing(*arg):
    pass

def scale(img, scale=0.5):
    return cv2.resize(img, (0,0), fx=scale, fy=scale)

def prepare(file):
    img = cv2.imread(file)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV);
    norm = img[:,:,1]
    return img, norm

def runTestingStream(foldername):
    # Run looped images from the folder with some
    # Trackbars allowing easy but intensive
    # parameters investiagion
    files = glob(foldername + '/*.jpg')
    norm = cv2.imread(files[0])

    # First create window
    # Make thresholidng window with slider to expermient live
    cv2.namedWindow('Threshold')
    cv2.createTrackbar('thresh1', 'Threshold', 97, 255, nothing)
    cv2.createTrackbar('thresh2', 'Threshold', 40, 255, nothing)
    # Window loop in a loop
    inloop = True
    beg = 1100
    end = 1200
    it = beg
    while inloop:
        for it in range(beg,end):
            im1, t1 = prepare(files[it])
            im2, t2 = prepare(files[it+1])
            print it
            thresh1 = cv2.getTrackbarPos('thresh1','Threshold')
            thresh2 = cv2.getTrackbarPos('thresh2','Threshold')
            ret, t1 = cv2.threshold(t1, thresh1, 255, \
                    cv2.THRESH_BINARY)
            ret, t2 = cv2.threshold(t2, thresh1, 255, \
                    cv2.THRESH_BINARY)
            norm = cv2.absdiff(t1,t2)
            c, h = cv2.findContours(norm,cv2.RETR_TREE,\
                                    cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(im1, c, -1, (0,255,0),2)
            cv2.imshow('Threshold', scale(im1))
            key = cv2.waitKey(2)

            if key == 27:
                inloop = False
                break

    cv2.destroyAllWindows()
    return norm
