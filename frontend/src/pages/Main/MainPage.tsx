import React, {useState} from 'react';
import styles from './MainPage.module.scss';
import classNames from "classnames";
import Grid from '@material-ui/core/Grid';
import backgroundGreenGradient from '../../assets/images/background-green-gradient.png';
import {Icon, CircularProgress} from '@material-ui/core';
import axios from 'axios';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faCloudUploadAlt} from '@fortawesome/free-solid-svg-icons'

const MainPage = () => {
    const cx = classNames.bind(styles);
    const [loading, setLoading] = useState(false);
    const [showUploadImageForm, setShowUploadImageForm] = useState(true);

    async function onSendLinks() {
        setLoading(true);
        const response = await axios.post('https://postman-echo.com/post', {hello: 'hello'},);
        setLoading(false);
        setShowUploadImageForm(true);
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

                    {/*TODO: change text input after button clicked*/}
                    {!showUploadImageForm && <>
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
                    {/*TODO: upload Image*/}
                    {
                        showUploadImageForm &&
                        <>
                            <div className={cx(styles.uploadImageButton)}>
                                {/*<Icon>*/}
                                {/*    backup*/}
                                {/*</Icon>*/}
                                <FontAwesomeIcon style={{fontSize: '52px'}} icon={faCloudUploadAlt}/>

                                {/*TODO: add spinner when loading*/}
                                {/*<CircularProgress style={{color: 'white'}} size={50} />*/}
                            </div>
                            <div className={cx(styles.infoBeforeUpdload)}>

                            </div>
                        </>
                    }
                </div>
            </Grid>
        </Grid>
    );
};

export {MainPage};
