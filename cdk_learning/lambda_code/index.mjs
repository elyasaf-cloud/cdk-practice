import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";
const s3 = new S3Client({});

export async function handler(event, _context) {
  const bucketName = process.env.BUCKET_NAME;
  const objectName = event.pathParameters["file-name"];
  try {
    const data = await s3.send(new GetObjectCommand({ Bucket: bucketName, Key: objectName }));
    const fileText = await data.Body.transformToString();

    return {
      statusCode: 200,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        content: fileText,
      }),
    };
  } catch (error) {
    console.error(error.message)
    
    if (error.name === "NoSuchKey")
    {
      return {
      statusCode: 404,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: `File doesn't exist -> Bucket - ${bucketName}, key - ${objectName}`,
      }),
    };
    }
    
    return {
      statusCode: 500,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: `Error -> ${error.message}`,
      }),
    };
  }
}
