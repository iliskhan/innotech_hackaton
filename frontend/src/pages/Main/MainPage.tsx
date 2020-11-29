import React, { useState } from 'react';
import classNames from "classnames";
import Grid from '@material-ui/core/Grid';
import { Redirect } from 'react-router-dom';
import { CircularProgress } from '@material-ui/core';
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCloudUploadAlt } from '@fortawesome/free-solid-svg-icons'

import styles from './MainPage.module.scss';
import backgroundGreenGradient from '../../assets/images/background-green-gradient.png';

const MainPage = () => {
    const cx = classNames.bind(styles);
    const [loading, setLoading] = useState(false);
    const [showUploadImageForm, setShowUploadImageForm] = useState(false);
    // const [filePhoto, setFilePhoto] = useState<{
    //     file: File;
    //     binary: string | ArrayBuffer | null;
    // } | null>();
    const [response, setResponse] = useState<any>();

    async function onSendLinks() {
        setLoading(true);

        // TODO: change to real 'endpoint' and 'payload'
        await axios.post('https://postman-echo.com/post', {hello: 'hello'});
        setLoading(false);
        setShowUploadImageForm(true);
    }

    // function to read file as binary and return
    function getFileFromInput(file: File): Promise<any> {
        return new Promise(function (resolve, reject) {
            const reader = new FileReader();
            reader.onerror = reject;
            reader.onload = function () {
                resolve(reader.result);
            };
            reader.readAsBinaryString(file); // here the file can be read in different way Text, DataUrl, ArrayBuffer
        });
    }

    async function handleFileUpload(e: React.ChangeEvent<HTMLInputElement>) {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            setLoading(true);
            const file = e.target.files[0];
            const binary = await getFileFromInput(file);

            const formData = new FormData();
            // formData.append('name', name ? name : 'uploaded_image');
            formData.append('file', file);
            // TODO: change to real 'endpoint'
            const response = await axios.post('https://postman-echo.com/post', formData);
            console.log(response)
            setResponse(response.data);
            // setFilePhoto({
            //     file,
            //     binary,
            // })

        }
    }

    if (response) {
        return <Redirect
            to={{
                pathname: "/user-info",
                state: { referrer: response }
            }}
        />
    }

    return (
        <Grid className={cx(styles.container)} container
        >
            <Grid className={cx(styles.containerItem)} item xs={7}>
                <div className={cx(styles.leftItemContainer)}>
                    <div>
                        <h1>Invenient<br/> Face</h1>
                        <p>INNOTECH HACK</p>
                    </div>
                </div>
            </Grid>
            <Grid style={{
                background: `url(${backgroundGreenGradient})`,
                backgroundPosition: 'center',
                backgroundSize: 'cover'
            }} className={cx(styles.containerItem)} item xs={5}>
                <div className={cx(styles.rightItemContainer)}>
                    <p className={cx(styles.itemTitle)}>
                        Сервис для идентификации по фотографии клиентов
                        банка и сбора их финансового профиля из различных открытых источников.
                    </p>
                    <Grid className={cx(styles.progressStepsContainer)} container alignItems="center">
                        <Grid item xs={2}>
                            <span
                                className={cx(styles.progressStep, {[styles.notActive]: showUploadImageForm})}>1</span>
                        </Grid>
                        <Grid item className={cx(styles.progressMessage)} xs={8}>
                            {!showUploadImageForm ? 'Добавьте ссылки' : 'Загрузите фото для поиска'}
                        </Grid>
                        <Grid item xs={2}>
                            <span
                                className={cx(styles.progressStep, {[styles.notActive]: !showUploadImageForm})}>2</span>
                        </Grid>
                    </Grid>

                    {
                        showUploadImageForm ? <>
                            <input
                                id="file"
                                type="file"
                                onChange={(e) => handleFileUpload(e)}
                                className={cx(styles.inputFileField)}
                                disabled={loading}
                            />
                            <label htmlFor="file">
                                <div className={cx(styles.uploadImageButton, {[styles.notActive]: loading})}>
                                    {
                                        !loading ?
                                            < FontAwesomeIcon style={{fontSize: '52px'}} icon={faCloudUploadAlt}/>
                                            :
                                            <CircularProgress style={{color: 'white'}} size={50}/>
                                    }
                                </div>
                            </label>
                            <div className={cx(styles.infoBeforeUpdload)}>

                            </div>
                        </> : <>
                        <textarea rows={12} className={cx(styles.textArea, {[styles.notActive]: loading})}>
                        </textarea>
                            <button disabled={loading} onClick={onSendLinks}
                                    className={cx(styles.submitLinksButton, {[styles.notActive]: loading})}>
                             <span className={cx({[styles.hide]: loading})}>
                                ОТПРАВИТЬ
                             </span>
                                {loading && <CircularProgress
                                    style={{
                                        color: 'white',
                                        position: 'absolute',
                                        right: '43%',
                                        top: '17px'
                                    }} size={16}/>}
                            </button>
                        </>
                    }

                </div>
            </Grid>
        </Grid>
    );
};

export {MainPage};
