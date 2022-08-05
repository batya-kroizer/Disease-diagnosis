import './Image.css';

export default function Image(props){
  
const createCropPreview = async (image, crop, fileName) => {
    const scaleX = image.naturalWidth / image.width;
    const scaleY = image.naturalHeight / image.height;
    const canvas = document.createElement("canvas");

    canvas.width = Math.ceil(crop.width * scaleX);
    canvas.height = Math.ceil(crop.height * scaleY);

    const ctx = canvas.getContext("2d");

    ctx.drawImage(
      image,
      crop.x * scaleX,
      crop.y * scaleY,
      crop.width * scaleX,
      crop.height * scaleY,
      0,
      0,
      crop.width * scaleX,
      crop.height * scaleY
    );

    return new Promise((resolve, reject) => {
      canvas.toBlob((blob) => {
        if (blob) {
          blob.name = fileName;
          window.URL.revokeObjectURL(previewUrl);
          const obj = window.URL.createObjectURL(blob);
          setPreviewUrl(obj);
          props.setImg(obj, blob);
        }
      }, "image/jpeg");
    });
  };
    return(

     <div
       id="carouselBasicExample"
       className="carousel slide carousel-fade"
       data-bs-ride="carousel"
     >
       <div className="carousel-indicators">
       {props.image.map((img,index)=>index==0?
         <button
           type="button"
           data-bs-target="#carouselBasicExample"
           data-bs-slide-to={index}
           className="active"
           aria-current="true"
           aria-label="Slide "{...+index+1}
         ></button>
         :<button
           type="button"
           data-bs-target="#carouselBasicExample"
           data-bs-slide-to={index}
           aria-label="Slide "{...+index+1}
         ></button>)}
       </div>
       <div className="carousel-inner">
       {props.image.map((img,index)=>index==0? 
       <div className="carousel-item active"><img src={img} className="my-img d-block w-100 img-thumbnail" /><div className="carousel-caption d-none d-md-block"></div></div>
       :<div className="carousel-item"> <img src={img} className="my-img d-block w-100 img-thumbnail" /><div className="carousel-caption d-none d-md-block"></div></div>)}
       <button
         className="carousel-control-prev"
         type="button"
         data-bs-target="#carouselBasicExample"
         data-bs-slide="prev"
       >
         <span className="carousel-control-prev-icon" aria-hidden="true"></span>
         <span className="visually-hidden">Previous</span>
       </button>
       <button
         className="carousel-control-next"
         type="button"
         data-bs-target="#carouselBasicExample"
         data-bs-slide="next"
       >
         <span className="carousel-control-next-icon" aria-hidden="true"></span>
         <span className="visually-hidden">Next</span>
       </button>
     </div>
     </div>

     
    )
}