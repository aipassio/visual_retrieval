import styles from './reid.css';
import {Col, Divider, Image, Row} from "antd";
import {useState} from "react";
import ImportId from "@/pages/ImportId";
import Retrieval from "@/pages/Retrieval";
import {fallbackImage} from "@/pages/util";


export default function () {
  const [
    currentImage,
    setCurrentImage
  ] = useState(fallbackImage)

  const [results, setResults] = useState([])

  const [previewImage, setPreviewImage] = useState(fallbackImage);
  return (
    <>
      <div className={styles.siteLayoutContent}>
        <Row>
          <Col span={16}>
            <Row>
              <Image
                width="650px"
                height="650px"
                src={currentImage}
                fallback={fallbackImage}
              />
            </Row>
            <Divider/>
            <Row>
              <Col span={24} style={{overflowX: "scroll", width: "100%"}}>
                {results.map((result, index) => <><Image
                  key={index}
                  preview={false}
                  style={{cursor: "pointer"}}
                  onClick={(item) => {
                    setCurrentImage("data:image/jpeg;base64," + result.image)
                  }}
                  width="64px"
                  height="64px"
                  src={"data:image/jpeg;base64," + result.image}
                  fallback={fallbackImage}
                />&nbsp;</>)}
              </Col>
            </Row>
          </Col>
          <Col span={8} style={{paddingLeft: 15}}>
            <Retrieval setResults={(results) => {
              if (results.length <= 0) {
                return
              }
              setCurrentImage("data:image/jpeg;base64," + results[0].image)
              setResults(results)
            }}/>
            <Divider/>
            <ImportId/>
          </Col>
        </Row>
      </div>
    </>
  );
}
