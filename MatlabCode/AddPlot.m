function imgname = AddPlot(doc, name)
import mlreportgen.dom.*;

imgtype = '-dpng';
imgname= [name '.png'];

% Convert figure to the specified image type.
print(imgtype, imgname);

% Set image height and width.
img = Image(imgname);
img.Width = '5in';
img.Height = '4in';

% Append image to document.
append(doc, Paragraph(img));

% Delete plot figure window.
delete(gcf);

end
